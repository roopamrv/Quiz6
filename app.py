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

# # Create table if it doesn't exist
# with conn.cursor() as cursor:
#     cursor.execute("""
#         CREATE TABLE stock (
#             id INT IDENTITY(1,1) PRIMARY KEY,
#             item_name VARCHAR(100) NOT NULL
#         )
#     """")
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

    # Split the command into parts
    parts = command.split()

    # Check the command type
    if parts[0] == 'P':
        # Put item into inventory
        item = parts[1]
        print(item)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO stock (item_name) VALUES (?)", (item))
            conn.commit()
    elif parts[0] == 'G':
        # Get item from inventory
        item = parts[1]
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM stock WHERE item_name = (?)", (item))
            result = cursor.fetchone()
            if result:
                item_id = result[0]
                cursor.execute("DELETE FROM stock WHERE id = (?)", (item_id))
                conn.commit()
                return f'[{request.form["shopper"]}] G {item}'
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
        return 'Not implemented'  # Modify this part to fetch and display transactions from a separate table
    else:
        return 'Invalid command.'

    return 'Command processed successfully.'

if __name__ == '__main__':
    app.run(debug=True)
