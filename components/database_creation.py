import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def connect_to_database():
    try:
        db = mysql.connector.connect(**config)
        return db
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None



def create_database():
    db = mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"]
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS WaterQualityMonitoringSystem")
    cursor.close()
    db.close()

def create_user_table(current_username):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("USE WaterQualityMonitoringSystem")
    create_user_table_query = f"""
    CREATE TABLE IF NOT EXISTS {current_username}_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        aluminium FLOAT,
        ammonia FLOAT,
        arsenic FLOAT,
        barium FLOAT,
        cadmium FLOAT,
        chloramine FLOAT,
        chromium FLOAT,
        copper FLOAT,
        flouride FLOAT,
        bacteria FLOAT,
        viruses FLOAT,
        `lead` FLOAT,
        nitrates FLOAT,
        nitrites FLOAT,
        mercury FLOAT,
        perchlorate FLOAT,
        radium FLOAT,
        selenium FLOAT,
        silver FLOAT,
        uranium FLOAT,
        is_safe INT
    )
    """
    cursor.execute(create_user_table_query)
    db.commit()
    cursor.close()
    db.close()
    # st.write(f'{current_username}_data table was created')

def insert_user_inputs(current_username, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("USE WaterQualityMonitoringSystem")
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    insert_new_data_query = f"""
    INSERT INTO {current_username}_data (timestamp, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, `lead`, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    insert_new_data = (current_timestamp, aluminium, ammonia, arsenic, barium, cadmium, chloramine, chromium, copper, flouride, bacteria, viruses, lead, nitrates, nitrites, mercury, perchlorate, radium, selenium, silver, uranium, is_safe)
    cursor.execute(insert_new_data_query, insert_new_data)
    db.commit()
    cursor.close()
    db.close()
    st.write("Record has been saved successfully.")
    


def show_user_table(current_username):
    db = connect_to_database()
    cursor = db.cursor()

    cursor.execute("USE WaterQualityMonitoringSystem")
    select_query = f"SELECT * FROM {current_username}_data"
    cursor.execute(select_query)
    records = cursor.fetchall()

    cursor.close()
    db.close()

    if records:
        df = pd.DataFrame(records, columns=['id','timestamp', 'aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper', 'flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium','is_safe'])
        with st.expander('🔎 Personal Feed - Database'):
            st.data_editor(df,hide_index=True, disabled=("id","timestamp","is_safe"))
    else:
        st.write("No Feed is recorded yet... Go and use Predicting Model for personal feed.")
    
    


def get_database(current_username):
    db = connect_to_database()
    cursor = db.cursor()

    cursor.execute("USE WaterQualityMonitoringSystem")
    select_query = f"SELECT * FROM {current_username}_data"
    cursor.execute(select_query)
    records = cursor.fetchall()

    cursor.close()
    db.close()

    if records:
        df = pd.DataFrame(records, columns=['id','timestamp', 'aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper', 'flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium','is_safe'])
    
    return df
