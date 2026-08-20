# db.py
import pyodbc

CONN_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=products;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

def get_db_connection():
    return pyodbc.connect(CONN_STRING)