import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
import sqlite3
import pandas as pd


# Settings
incomes = ["Salary","Part Time","Other Income"]
expenses = ["Rent","Utilities","Groceries","Other Expenses","Savings"]
currency="USD"
page_title ="Expense Tracker"
title="Money Management Made Easy"
title_icon=":money_with_wings:"
page_icon=":money_mouth_face:"
layout="centered"


st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(title+ " " + title_icon)

years=[datetime.today().year, datetime.today().year+1]
months = list(calendar.month_name[1:])



st.subheader(f"Entering dollars in the most amusing manner for my app: {currency}ata Input! 😂 ")
with st.form("entry_form",clear_on_submit=True):
    col1,col2 = st.columns(2)
    col1.selectbox("Select Month:",months,key="month")
    col2.selectbox("Select Year:",years,key="year")
    "---"

    with st.expander("Income"):
        for income in incomes:
            st.number_input(f"{income}:",min_value=0,format="%i",step=10,key=income)

    with st.expander("Expenses"):
        for expense in expenses:
            st.number_input(f"{expense}:",min_value=0,format="%i",step=10,key=expense)

    with st.expander("Comments"):
        comment=st.text_area("",placeholder="Enter a comment here ...")

    "---"
    submitted=st.form_submit_button("Save")



# Database Connectivity


conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        year INTEGER,
        salary INTEGER,
        part_time INTEGER,
        other_income INTEGER,
        rent INTEGER,
        utilities INTEGER,
        groceries INTEGER,
        other_expenses INTEGER,
        savings INTEGER,
        comments TEXT
    )
''')
conn.commit()

# Insert data into the database upon form submission
if submitted:
    month = st.session_state.month
    year = st.session_state.year
    values = [month, year] + [st.session_state[income] for income in incomes] + [st.session_state[expense] for expense in expenses] + [comment]
    cursor.execute('''
        INSERT INTO expenses (month, year, salary, part_time, other_income, rent, utilities, groceries, other_expenses, savings, comments)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)
    conn.commit()
    st.success("Data saved successfully!")


conn.close()


# Data Visualization Button
show_viz_button = st.button("Visualize It")



if show_viz_button:
    st.header("Data Visualization")


    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM expenses
    ''')
    data = cursor.fetchall()
    conn.close()

    print("Retrieved Data:", data)


    if data:
        df = pd.DataFrame(data, columns=["ID", "Year", "Month"] + incomes + expenses + ["Comment"])
        st.subheader("Your Previous Entries :")
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}))


        categories = incomes + expenses
        values = [sum(df[income]) for income in incomes] + [sum(df[expense]) for expense in expenses]


        fig_pie = go.Figure()
        fig_pie.add_trace(go.Pie(labels=categories, values=values, hole=0.3))
        fig_pie.update_layout(title=f"Overall Breakdown")
        st.plotly_chart(fig_pie)
    else:
        st.warning("No data available.")

clear_database_button = st.button("Clear All Entries")

if clear_database_button:
    conn = sqlite3.connect("expense_tracker.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    conn.close()
    st.success("All entries cleared !")

