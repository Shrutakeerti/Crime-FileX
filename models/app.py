# app.py
import streamlit as st
import requests

# Set up backend URL
backend_url = "http://localhost:5000"

# Login page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Implement actual login logic here
        st.success("Logged in successfully")

# Add/Delete Cases page
def manage_cases():
    st.title("Add/Delete Cases")
    case_id = st.text_input("Case ID")
    name = st.text_input("Suspect Name")
    blood_group = st.selectbox("Blood Group", ["A", "B", "AB", "O"])
    dna = st.text_area("Enter DNA Information")
    retina_scan = st.file_uploader("Upload Retina Scan", type=["jpg", "png"])
    fingerprint = st.file_uploader("Upload Fingerprint", type=["jpg", "png"])
    photos = st.file_uploader("Upload Suspect Photos (3 views)", accept_multiple_files=True, type=["jpg", "png"])

    if st.button("Add Case"):
        case_data = {
            "case_id": case_id,
            "name": name,
            "blood_group": blood_group,
            "dna": dna,
            "retina_scan": retina_scan,
            "fingerprint": fingerprint,
            "photos": photos
        }
        response = requests.post(f"{backend_url}/add_case", json=case_data)
        st.write(response.json()["status"])

# Crime Pattern Analysis page
def crime_pattern_analysis():
    st.title("Crime Pattern Analysis")
    input_data = st.text_area("Enter Data for Analysis")
    if st.button("Analyze Pattern"):
        response = requests.post(f"{backend_url}/crime_pattern_analysis", json={"data": input_data})
        st.write(response.json()["pattern"])

# Chatbot page
def chatbot():
    st.title("Chatbot")
    user_message = st.text_input("You: ")
    if st.button("Send"):
        response = requests.post(f"{backend_url}/chatbot", json={"message": user_message})
        st.write("Bot:", response.json()["response"])

# Main
def main():
    st.sidebar.title("Criminal Record Management System")
    page = st.sidebar.selectbox("Choose a page", ["Login", "Manage Cases", "Crime Pattern Analysis", "Chatbot"])

    if page == "Login":
        login()
    elif page == "Manage Cases":
        manage_cases()
    elif page == "Crime Pattern Analysis":
        crime_pattern_analysis()
    elif page == "Chatbot":
        chatbot()

if __name__ == "__main__":
    main()
