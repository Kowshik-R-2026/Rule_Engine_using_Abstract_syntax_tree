import streamlit as st
import ast_parse  # Import the ast_parse.py module
import sqlite3
import pandas as pd

st.set_page_config(layout="wide", page_title='Rule Engine using Abstract tree')

# Function to fetch rules from rules.db
def fetch_rules():
    conn = sqlite3.connect('rules.db')
    query = "SELECT rule FROM rules"
    df = pd.read_sql(query, conn)
    conn.close()
    return df['rule'].tolist()

# Function to insert a new rule into rules.db and return if it was successful
def store_rule(rule):
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO rules (rule) VALUES (?)", (rule,))
        conn.commit()
        return True  # Successfully stored
    except sqlite3.IntegrityError:
        return False  # Rule already exists
    finally:
        conn.close()

# Function to delete a rule from rules.db
def delete_rule(rule):
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rules WHERE rule=?", (rule,))
    conn.commit()
    conn.close()

# Function to fetch employee data with optional rule filtering
def fetch_employee_data(rule=None):
    conn = sqlite3.connect('employee.db') 
    if rule:
        query = f"SELECT * FROM employee WHERE {rule}"
    else:
        query = "SELECT * FROM employee"
    df = pd.read_sql(query, conn) 
    conn.close()  
    return df

# Initialize session state for selected rule if it doesn't exist
if 'selected_rule' not in st.session_state:
    st.session_state.selected_rule = None

# Fetch previous rules from rules.db
previous_rules = fetch_rules()

# Layout for the main display
col1, col2, col3 = st.columns([2, 3, 2])

# Database Display (left side)
with col2:
    st.subheader("Database Display")
    
    # Fetch and display employee database content
    employee_data = fetch_employee_data() 
    st.dataframe(employee_data)

    # Dropdown for previous rules with Add and Delete buttons
    st.write("**Previous Rules**")
    selected_rule_from_dropdown = st.selectbox("Select a rule to add or delete", options=previous_rules)
    
    col_add, col_delete = st.columns([1, 1])

    with col_add:
        # Add button: When clicked, it adds the selected rule to the rule_input field
        if st.button("✙  Add Rule", key=f"add_{selected_rule_from_dropdown}"):
            st.session_state.selected_rule = selected_rule_from_dropdown

    with col_delete:
        # Delete button: When clicked, it deletes the selected rule from the database
        if st.button("🗑️ Delete Rule", key=f"delete_{selected_rule_from_dropdown}"):
            delete_rule(selected_rule_from_dropdown)
            st.experimental_rerun()  # Refresh the app after deletion

    # Rule Input and Evaluate Button (bottom side)
    rule_input = st.text_input("Rule Input", placeholder="Enter your rule here", value=st.session_state.selected_rule if st.session_state.selected_rule else "")
    ast_json, parse_tree = None, None
    error_message = ""

    if st.button("Create Syntax Tree"):
        # Get AST and Parse Tree from ast_parse.py
        ast_json, parse_tree = ast_parse.get_ast_and_parse_tree(rule_input)

        # Validate the AST before storing the rule
        if ast_json and parse_tree:
            if store_rule(rule_input):  # Store the rule if valid
                st.success("Rule stored successfully!")
                
                # Refresh the list of previous rules
                previous_rules = fetch_rules()  # Update previous rules after storing
                # Update selected rule in session state
                st.session_state.selected_rule = rule_input  # Set the newly added rule as selected
            else:
                st.error("Rule already exists: Please enter a different rule.")
        else:
            error_message = "Invalid rule: Please check the syntax."
            rule_input = "" 

    # Display error message if any
    if error_message:
        st.error(error_message)

# AST Display and Parse Tree (right side)
with col1:
    st.subheader("AST Display")
    if ast_json:
        st.json(ast_json)

with col3:
    st.subheader("Filtered Database Display")
    filtered_data = fetch_employee_data(rule=rule_input)
    st.dataframe(filtered_data, use_container_width=True)

    st.subheader("Parse Tree")
    if parse_tree:
        st.text("\n".join(parse_tree))
