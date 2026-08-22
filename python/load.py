import psycopg


connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="call_reports",
    user="furwil",
    password="1234"
)

print("Successfully connected to PostgreSQL!")

connection.close()

