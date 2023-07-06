# from flask import Flask, render_template, request
# import pyodbc

# app = Flask(__name__)

# # SQL Database connection details
# db_server = 'tcp:roopamdb.database.windows.net'
# db_name = 'demodb'
# db_user = 'adminuser'
# db_password = 'Test@123'

# # Establish the database connection
# conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={db_server};Database={db_name};UID={db_user};PWD={db_password}"
# conn = pyodbc.connect(conn_str)


# # Global variables
# inventory = []
# transactions = []

# # Route for home page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Route for processing commands
# @app.route('/process', methods=['POST'])
# def process():
#     global inventory, transactions

#     # Get command from the form
#     command = request.form['command']

#     # Split the command into parts
#     parts = command.split()

#     # Check the command type
#     if parts[0] == 'P':
#         # Put item into inventory
#         item = parts[1]
#         inventory.append(item)
#     elif parts[0] == 'G':
#         # Get item from inventory
#         item = parts[1]
#         if item in inventory:
#             inventory.remove(item)
#             transactions.append(f'[{request.form["shopper"]}] G {item}')
#         else:
#             return 'Item not available.'
#     elif parts[0] == 'I':
#         # Show inventory
#         return ', '.join(inventory)
#     elif parts[0] == 'T':
#         # Show transactions
#         return '\n'.join(transactions)
#     else:
#         return 'Invalid command.'

#     return 'Command processed successfully.'

# if __name__ == '__main__':
#     app.run(debug=True)
