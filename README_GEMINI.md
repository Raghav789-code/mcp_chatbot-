# People Directory Chatbot with Gemini AI

## 🚀 Quick Start

### Option 1: Easy Setup (Recommended)
```bash
python setup_gemini.py
```
Then paste your Gemini API key when prompted.

### Option 2: Manual Setup
1. Edit the `.env` file
2. Replace `your_gemini_api_key_here` with your actual API key

### Option 3: Windows Users
Double-click: `start_with_gemini.bat`

## 🔑 Get Your FREE Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

## 🎯 Run the Chatbot

```bash
python chatbot/app.py
```

Open browser: http://localhost:8002

## ✨ Features

- **With API Key**: Full conversational AI using Gemini
- **Without API Key**: Smart pattern matching (still works!)
- **CSV Integration**: Reads from your CSV files
- **Natural Language**: Ask questions naturally

## 💬 Try These:

- "Who is John Smith?"
- "Find Sarah"
- "List all managers"
- "Show people in Sales department"
- "Details of David Johnson"

## 📁 Your Data

Put your CSV files in the `data/` folder with columns:
- id, full_name, preferred_name, email, phone, role, department, location, tags

The system will automatically detect and use your CSV files!