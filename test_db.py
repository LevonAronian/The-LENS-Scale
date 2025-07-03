import streamlit as st
import gspread
import pandas as pd

st.set_page_config(title="Database Connection Test", layout="centered")
st.title("Database Connection Test 🧪")

# This is the function we want to test
@st.cache_resource
def connect_to_gsheet():
    try:
        creds = st.secrets["gcp_service_account"]
        st.write("Successfully loaded `gcp_service_account` from secrets.")
    except Exception as e:
        st.error("Failed to load `gcp_service_account` from Streamlit Secrets.")
        st.error(f"Error details: {e}")
        st.stop()
        
    try:
        gc = gspread.service_account_from_dict(creds)
        st.write("Successfully authenticated with Google using credentials.")
    except Exception as e:
        st.error("Failed to authenticate with Google. Your `private_key` or other credentials might be formatted incorrectly.")
        st.error(f"Error details: {e}")
        st.stop()
        
    try:
        # IMPORTANT: Make sure this name is EXACTLY right.
        spreadsheet = gc.open("MovieRatingsDB")
        st.write("Successfully opened the spreadsheet named 'MovieRatingsDB'.")
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("ERROR: SpreadsheetNotFound. Could not find a Google Sheet named 'MovieRatingsDB'. Please check the name and sharing permissions.")
        st.stop()
    except Exception as e:
        st.error("An unknown error occurred while trying to open the spreadsheet.")
        st.error(f"Error details: {e}")
        st.stop()
        
    try:
        worksheet = spreadsheet.worksheet("Sheet1")
        st.write("Successfully opened the tab named 'Sheet1'.")
    except gspread.exceptions.WorksheetNotFound:
        st.error("ERROR: WorksheetNotFound. Could not find a tab named 'Sheet1' in your spreadsheet.")
        st.stop()
    except Exception as e:
        st.error("An unknown error occurred while trying to open the 'Sheet1' tab.")
        st.error(f"Error details: {e}")
        st.stop()
        
    return worksheet

# --- Main Test Logic ---
st.header("1. Attempting to Connect")
worksheet = connect_to_gsheet()
st.success("✅ Connection Successful!")

st.header("2. Attempting to Read Data")
try:
    all_data = pd.DataFrame(worksheet.get_all_records())
    st.write("Successfully read data from the worksheet.")
    st.success("✅ Data Reading Successful!")
    
    st.header("3. Displaying Raw Data from Database")
    st.write("If you see your data below, the connection is working perfectly.")
    st.dataframe(all_data)
    
except Exception as e:
    st.error("Failed to read data from the worksheet into a DataFrame.")
    st.error("This usually means the sheet is empty or the headers are missing.")
    st.error(f"Error details: {e}")
