from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# SQL Database connection details
db_server = 'tcp:roopamdb.database.windows.net'
db_name = 'demodb'
db_user = 'adminuser'
db_password = 'Test@123'

# Establish the database connection
conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={db_server};Database={db_name};UID={db_user};PWD={db_password}"
conn = pyodbc.connect(conn_str)

# # Create tables if they don't exist
# with conn.cursor() as cursor:
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS stock (
#             id INT IDENTITY(1,1) PRIMARY KEY,
#             item_name VARCHAR(100) NOT NULL
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS transactions (
#             id INT IDENTITY(1,1) PRIMARY KEY,
#             shopper_name VARCHAR(100) NOT NULL,
#             item_name VARCHAR(100) NOT NULL
#         )
#     """)
#     conn.commit()

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for processing commands
@app.route('/process', methods=['POST'])
def process():
    # Get command from the form
    command = request.form['command']
    shopper = request.form['shopper']

    # Split the command into parts
    parts = command.split()

    # Check the command type
    if parts[0] == 'P':
        # Put item into inventory
        item = parts[1]
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO stock (item_name) VALUES (?)", item)
            cursor.execute("INSERT INTO transactions (item_name) VALUES (?)", item)
            conn.commit()
    elif parts[0] == 'G':
        # Get item from inventory
        item = parts[1]
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM stock WHERE item_name = (?)", (item))
            result = cursor.fetchone()
            if result:
                item_id = result[0]
                cursor.execute("DELETE FROM stock WHERE id = ?", item_id)
                cursor.execute("INSERT INTO transactions (shopper_name, item_name) VALUES (?, ?)", shopper, item)
                conn.commit()
                return f'[{shopper}] G {item}'
            else:
                return 'Item not available.'
    elif parts[0] == 'I':
        # Show inventory
        with conn.cursor() as cursor:
            cursor.execute("SELECT item_name FROM stock")
            result = cursor.fetchall()
            inventory = [row[0] for row in result]
            return ', '.join(inventory)
    elif parts[0] == 'T':
        # Show transactions
        with conn.cursor() as cursor:
            cursor.execute("SELECT shopper_name, item_name FROM transactions ORDER BY id")
            result = cursor.fetchall()
            transactions = [f'[{row[0]}] G {row[1]}' for row in result]
            return '\n'.join(transactions)
    else:
        return 'Invalid command.'

    return 'Command processed successfully.'

if __name__ == '__main__':
    app.run(debug=True)
