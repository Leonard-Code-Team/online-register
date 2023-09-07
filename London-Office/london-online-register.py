import streamlit as st
from datetime import datetime, timedelta
from deta import Deta
import pandas as pd
import streamlit_authenticator as stauth

# List of Employees

employees = st.secrets['london_employees']['employees']


sorted_employees = sorted(employees)

# Webpage

st.title(':green[Leonard Design Architects]')

col1, col2 = st.columns(2)

with col1:
   st.subheader("London Studio")


with col2:
    date = datetime.today().strftime("%B %d, %Y")
    today = "Date: {}".format(date)
    st.subheader(today)

# Login authentication
authenticator = stauth.Authenticate(
    dict(st.secrets['credentials']),
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

#print(sorted(employees))

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

if authentication_status:
    authenticator.logout('Logout', 'main')
    # Dropdown selection box
    employee = st.selectbox(
        'sign in',
        ["select..."] + sorted_employees)

    visitor = st.text_input("Visitor sign in", value="Please enter your full name / organisation...")

    # signed_in_employees = dict()
    #
    # if employee not in signed_in_employees:
    #     signed_in_employees[employee] = datetime.now()

    #tomorrow = (datetime.now() + timedelta(days=15))

    # store employee signed-in details
    # Connect to Deta Base with your Data Key
    api_key = st.secrets['deta']['api_key']
    deta = Deta(api_key)

    # Create a new database "example-db"
    # If you need a new database, just use another name.
    db = deta.Base("London_Register")

    # If the user clicked the submit button,
    # write the data from the form to the database.
    # You can store any data you want here. Just modify that dictionary below (the entries between the {}).

    if employee != "select...":
        db.put({'Date': str(date)}, employee)

    if visitor != "Please enter your full name / organisation..." or visitor != "" or visitor is not None:
        db.put({'Date': str(date)}, visitor)


    # display who is in
    "People in the office:"
    # This reads all items from the database and displays them to your app.
    # db_content is a list of dictionaries. You can do everything you want with it.
    db_content = db.fetch().items

    # Only retrieve employees name if it is the current date
    employees_in = []
    for e in db_content:
        if e['Date'] == str(date):
            employees_in.append(e['key'])
    st.write(employees_in)

    # sign-out and remove people from list
    employee_in = st.selectbox(
        'sign out',
        ["select name and press enter..."] + employees_in)

    if employee_in != "select name and press enter...":
        db.delete(employee_in)

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')