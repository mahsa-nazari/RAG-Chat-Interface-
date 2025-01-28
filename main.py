import requests
import json
import streamlit as st
import os
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "25ae20b8-f47f-4f2c-9794-3e987c0f5fdd"
FLOW_ID = "a78a24be-6f89-4474-b1b2-86c480da2cff"
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = "customer" 

def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("Chat Interface")
    message = st.text_input("Message", placeholder="Enter your message here ...")
    if st.button("Send"):
        if not message.strip():
            st.warning("Please enter a message.")
            return
        try:
            with st.spinner("Processing ..."):
                response = run_flow(message)
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()