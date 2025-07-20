import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()


# ✅ Load cleaned restaurant data safely
csv_path = "Karachi_rest.csv"  # ✅ Updated file path

if not os.path.exists(csv_path):
    st.error(f"❌ File '{csv_path}' not found. Please make sure it’s saved as 'Karachi_rest.csv'.")
    st.stop()

df = pd.read_csv(csv_path)

# ✅ Gemini API setup (insert your key)
genai.configure(api_key=os.getenv("YOUR_GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.0-pro")

# 🎯 App title
st.title("🍽️ Foodpanda Restaurant Chatbot (Karachi)")

# 🔍 Search input or dropdown
restaurant_input = st.text_input("🔍 Enter a restaurant name:")
restaurant_select = st.selectbox("📋 Or pick from the list:", options=[""] + sorted(df.RestaurantName.unique()))

restaurant_name = restaurant_input.strip() or restaurant_select

# 📡 Show restaurant info and handle queries
if restaurant_name:
    if restaurant_name in df.RestaurantName.values:
        res_data = df[df.RestaurantName == restaurant_name].iloc[0]

        st.markdown(f"### 🍴 {res_data['RestaurantName']}")
        st.write(f"📍 City: {res_data['City']}")
        st.write(f"⭐ Rating: {res_data['Rating']}")
        st.write(f"👥 Reviews: {res_data['Reviews']}")
        st.write(f"🧾 Menu: {res_data['Menu']}")

        user_question = st.text_input("🤖 Ask about menu, price, rating etc:")

        if user_question:
            prompt = f"""
You are a helpful restaurant assistant. A user asked about "{restaurant_name}" in Karachi.
Here’s the available data:

City: {res_data['City']}
Rating: {res_data['Rating']}
Reviews: {res_data['Reviews']}
Menu: {res_data['Menu']}

User's question: "{user_question}"

Answer based only on this data. Do not invent or assume dishes.
"""

            try:
                response = model.generate_content(prompt)
                st.markdown("#### 💬 Chatbot Response")
                st.write(response.text.strip())
            except Exception as e:
                st.error(f"❌ Gemini API Error: {e}")
    else:
        st.warning("❌ Restaurant not found. Double-check spelling or use dropdown.")
