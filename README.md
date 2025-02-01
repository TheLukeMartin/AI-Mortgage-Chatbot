# 🏡 AI Mortgage & Real Estate Chatbot

This is an **AI-powered chatbot** that helps users with mortgage and real estate-related questions. It leverages **FastAPI for the backend** and **Streamlit for the frontend** while integrating OpenAI for chat responses and external APIs for mortgage and property data.

---

## **🚀 Features**
✅ **AI Chatbot** - Provides AI-powered responses for mortgage and real estate inquiries.  
✅ **Chat History** - Stores past interactions in an SQLite database.  
✅ **Mortgage Calculator** - Estimates monthly payments based on loan amount and interest rate.  
✅ **Zillow Property Search** - Retrieves property details based on the user's address.  

---

## **🛠 Installation Guide**
1️⃣ **Clone the Repository**
```sh
git clone https://github.com/TheLukeMartin/AI-Mortgage-Chatbot.git
cd AI-Mortgage-Chatbot

2️⃣ Create and Activate Virtual Environment

# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Create a .env File Create a .env file in the root directory to store API keys securely.

OPENAI_API_KEY=your_openai_api_key
MORTGAGE_API_HOST=mortgage-calculator-by-api-ninjas.p.rapidapi.com
MORTGAGE_API_KEY=your_mortgage_api_key
ZILLOW_API_HOST=zillow-com4.p.rapidapi.com
ZILLOW_API_KEY=your_zillow_api_key

💻 Running the 

1️⃣ Start the FastAPI Backend
Run the backend server with Uvicorn:

uvicorn backend:app --host 127.0.0.1 --port 8000 --reload

2️⃣ Start the Streamlit Frontend
Run the frontend:
streamlit run frontend.py

📌 API Endpoints
Method	Endpoint	Description
POST	/chat	Sends user input to the chatbot and returns an AI response
GET	/history	Retrieves the last 10 chat messages from history
GET	/mortgage	Estimates mortgage payments (params: loan_amount, interest_rate)
GET	/property	Searches property information (params: address)

🐛 Troubleshooting
Issue: "ModuleNotFoundError"
✅ Run: pip install -r requirements.txt

Issue: "uvicorn: command not found"
✅ Run: pip install uvicorn

Issue: "FastAPI or Streamlit not working"
✅ Restart your backend and frontend, and ensure the APIs are running.

📜 License
This project is licensed under the MIT License.


