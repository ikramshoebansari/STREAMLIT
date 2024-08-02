import streamlit as st
import mysql.connector
import os

# Set database connection details
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
DB_NAME = os.environ.get("DB_NAME", "tshirts")

def execute_query(query):
    """Executes the given SQL query and returns the results."""
    results = []
    conn = None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
        else:
            conn.commit()
            results = ["Query executed successfully"]
        cursor.close()
    except mysql.connector.Error as err:
        results = [f"Error executing query: {err}"]
    finally:
        if conn and conn.is_connected():
            conn.close()
    return results

# Streamlit application
st.title("SQL Query Executor")

st.markdown("""
Enter your SQL query in the text area below and click **Execute** to run the query. The results will be displayed below.
""")

user_query = st.text_area("SQL Query", height=150)

if st.button("Execute"):
    results = execute_query(user_query)
    if isinstance(results, list) and len(results) > 0:
        if isinstance(results[0], tuple):
            st.write("### Results")
            st.dataframe(results)
        else:
            st.write("### Message")
            for result in results:
                st.text(result)
    else:
        st.write("No results found or an error occurred.")
