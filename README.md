# Rule Engine Using Abstract Syntax Tree

This project implements a Rule Engine using an Abstract Syntax Tree (AST) to facilitate dynamic evaluation of business rules. The application is built with Streamlit and allows users to add, delete, and visualize rules stored in a SQLite database.

## Features

- Fetch and display employee data from a SQLite database.
- Add and delete rules stored in a separate SQLite database.
- Create and visualize an AST for rules input.
- Filter employee data based on user-defined rules.

## Installation

To set up the project, follow these steps:

1. **Clone the repository**

2. **Install the required packages:** `pip install -r requirements.txt`

3. **Set up the SQLite databases:**
- Ensure you have two SQLite databases: `rules.db` and `employee.db`.
- Create the `rules` table in `rules.db` if it doesn't exist:
  ```sql
  CREATE TABLE IF NOT EXISTS rules (
      rule TEXT PRIMARY KEY
  );
  ```

- Create the `employee` table in `employee.db` with the required schema to hold employee data.

4. **Run the application:**  `streamlit run app.py`

Replace `app.py` with the name of your main Streamlit application file.

## Usage

- Open the application in your web browser at the URL provided in the terminal.
- Use the interface to add or delete rules and visualize the AST for the input rules.
- Filter employee data based on the defined rules.

