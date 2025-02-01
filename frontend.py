# %%
import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"  # Ensure this matches your FastAPI server

# 🔹 Set Streamlit Page Layout
st.set_page_config(page_title="AI Mortgage Chatbot", layout="wide")

# 🔹 App Title
st.markdown("<h1 style='text-align: center;'>🏡 AI Mortgage & Real Estate Chatbot</h1>", unsafe_allow_html=True)

# 🔹 Sidebar - Chat History
st.sidebar.header("📜 Chat History")

try:
    history_response = requests.get(f"{API_URL}/history", timeout=5)
    if history_response.status_code == 200:
        chat_history = history_response.json().get("history", [])
        for entry in chat_history:
            st.sidebar.write(f"**User:** {entry['user']}")
            st.sidebar.write(f"**Bot:** {entry['bot']}")
            st.sidebar.write("---")
    else:
        st.sidebar.write("⚠️ Failed to load chat history.")
except requests.exceptions.RequestException:
    st.sidebar.write("⚠️ Backend is unreachable. Check if it's running.")

# 🔹 Store Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🔹 Chat Display Window
chat_window = st.container()
with chat_window:
    st.markdown("<div style='height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px;'>", unsafe_allow_html=True)
    for chat in st.session_state.chat_history:
        st.markdown(f"<div style='margin-bottom: 10px; padding: 10px; border-radius: 10px; background: #f3f3f3;'><b>User:</b> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-bottom: 10px; padding: 10px; border-radius: 10px; background: #d9fdd3;'><b>AI:</b> {chat['bot']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 🔹 User Input Field (DO NOT Modify `chat_input` Directly!)
user_input = st.text_input("💬 Type your message and press Enter:", key="chat_input")

# 🔹 Ensure messages are only processed once
if user_input and user_input != st.session_state.get("last_user_input", ""):
    st.session_state.last_user_input = user_input  # Store last input to prevent re-submission

    try:
        response = requests.post(f"{API_URL}/chat", json={"user_input": user_input}, timeout=10)
        if response.status_code == 200:
            chat_response = response.json().get("response", "I couldn't process that request.")

            # 🔹 Update Chat History
            st.session_state.chat_history.append({"user": user_input, "bot": chat_response})

            # 🔹 Force re-render UI to show new chat response
            st.rerun()
        else:
            st.error(f"⚠️ Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Connection Error: {e}")

# 🔹 Mortgage Calculator Section
st.header("📊 Mortgage Calculator")

loan_amount = st.number_input("🏦 Loan Amount ($)", value=200000, min_value=10000)
interest_rate = st.number_input("📈 Interest Rate (%)", value=3.5, min_value=0.1)

if st.button("📉 Get Mortgage Estimate"):
    try:
        mortgage_response = requests.get(
            f"{API_URL}/mortgage",
            params={"loan_amount": loan_amount, "interest_rate": interest_rate},
            timeout=10
        )
        if mortgage_response.status_code == 200:
            st.write("📊 **Estimated Mortgage:**")
            st.json(mortgage_response.json())
        else:
            st.error(f"⚠️ Error: {mortgage_response.status_code} - {mortgage_response.text}")
    except requests.exceptions.RequestException:
        st.write("⚠️ Could not connect to mortgage API.")

# 🔹 Zillow Property Search
st.header("🏠 Zillow Property Search")
address = st.text_input("📍 Enter a property address:")

if st.button("🔎 Search Property"):
    try:
        property_response = requests.get(
            f"{API_URL}/property",
            params={"address": address},
            timeout=10
        )
        if property_response.status_code == 200:
            st.write("🏡 **Property Information:**")
            st.json(property_response.json())
        else:
            st.write("⚠️ Error fetching property details.")
    except requests.exceptions.RequestException:
        st.write("⚠️ Could not connect to Zillow API.")

# %%
