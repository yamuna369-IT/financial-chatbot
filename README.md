💬 A GenAI-powered chatbot that extracts and analyzes financial data (revenue, income, assets, etc.) from 10-K/10-Q SEC filings for Apple, Microsoft, and Tesla using Python, Flask, and XML parsing with interactive chart visualizations.
# 💬 Financial Insights Chatbot

A GenAI-powered chatbot that extracts and analyzes financial data such as **revenue, net income, assets, liabilities, and more** from **10-K/10-Q XML filings** of **Apple, Microsoft, and Tesla**, using **Python**, **Flask**, and **XML parsing** with interactive **charts**.

---

## 🚀 Features

- 🤖 Natural language Q&A (e.g., "What was Apple's revenue in 2024?")
- 🏢 Company coverage: Apple, Microsoft, Tesla
- 📂 Extracts from SEC 10-K/10-Q XML files
- 🎨 Styled chat UI (WhatsApp-like interface)
- 🔍 Entity recognition for company, year, topic

---

## 📁 Project Structure

project/
│
├── app.py # Flask backend

├── chatbot_engine.py # Core chatbot logic

├── data_parser.py # XML data extraction

├── data/ # XML filings (Apple, Microsoft, Tesla)

│ └── aapl-20240629_htm.xml # Example file

│
├── templates/
│ └── index.html # Chat UI

│
├── static/
│ └── style.css # CSS styles (chat bubble style)

│
└── README.md

yaml
Copy
Edit

---




📌 Technologies Used
Python 🐍

Flask 🌐

HTML, CSS, JavaScript

Matplotlib & Seaborn 📊

XML Parsing with xml.etree.ElementTree

Regex-based Entity Extraction

