import os
import time
import pyttsx3
import streamlit as st
 
import google.generativeai as genai
import pandas as pd
 
API_KEY = 'AIzaSyA3WIq12WUKWHXlxYMHiCMsO5fz0IZNNGs'
genai.configure(api_key=API_KEY)
 
 
# Function to convert Excel to CSV
def convert_excel_to_csv(file_path):
    df = pd.read_excel(file_path)
    csv_path = file_path.replace(".xlsx", ".csv").replace(".xls", ".csv")
    df.to_csv(csv_path, index=False)
    return csv_path
 
# Function to analyze spending habits and provide advice
def analyze_spending_habits(file_path, prompt):
    # Convert Excel to CSV if needed
    if file_path.endswith((".xls", ".xlsx")):
        file_path = convert_excel_to_csv(file_path)
   
    # Upload the file
    customer_data_file = genai.upload_file(file_path)
    # Initialize a Gemini model appropriate for your use case
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # Create the prompt for spending habit analysis
    response = model.generate_content([prompt, customer_data_file])
   
    return response.text
 
# Function to save the uploaded file locally
def save_file_locally(uploaded_file):
    save_path = os.path.join("data", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path
 
# Function to read text aloud using pyttsx3
def read_text_aloud(text):
    engine = pyttsx3.init()
    # Optional: Change the voice to a female voice if available
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()
 
# Streamlit application
st.title("Standard Bank Personal Financial Advisor")
 
# Chat history placeholder
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
# File upload section
uploaded_file = st.file_uploader("Upload your spending data (CSV, Excel, or TXT)", type=["txt", "csv", "xls", "xlsx"])
 
# Check if a file is uploaded
if uploaded_file is not None:
    with st.spinner('Analyzing spending data...'):
        # Simulate processing time
        time.sleep(7)
 
# Extract and display analysis on button click
if prompt := st.chat_input("Enter your query (e.g., 'How can I save more based on my spending habits?')"):
    if uploaded_file is not None and prompt.strip() != "":
        file_path = save_file_locally(uploaded_file)
        result_text = analyze_spending_habits(file_path, prompt)
        st.session_state.chat_history.append({"prompt": prompt, "response": result_text})
    else:
        st.error("Please upload a spending data file and enter a query.")
 
# Display chat history
if st.session_state.chat_history:
    st.subheader("Advice History")
    for i, chat in enumerate(st.session_state.chat_history):
        st.write(f"**User:** {chat['prompt']}")
        st.write(f"**Financial Advisor:** {chat['response']}")
        if st.button(f"🔊 Listen to Advice {i+1}"):
            read_text_aloud(chat['response'])
        st.write("---")