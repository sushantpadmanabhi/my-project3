from flask import Flask, send_from_directory, request, jsonify
import pyodbc

# Azure SQL Database connection details
server = 'npl-project3-sqlserver.database.windows.net'
database = 'ncpl-project3-InventoryDB'
username = 'azureadmin'
password = 'N0vem8er@11:11'
driver = '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)

# Homepage route
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Update Inventory Page
@app.route('/update-inventory')
def update_inventory():
    return send_from_directory('.', 'update-inventory.html')

# Check Inventory Page
@app.route('/check-inventory')
def check_inventory():
    return send_from_directory('.', 'check-inventory.html')

# Function to establish a database connection
def get_db_connection():
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    )
    return connection


@app.route('/api/update-inventory', methods=['POST'])
def api_update_inventory():
    try:
        # Get JSON data from the request
        data = request.json
        product_name = data['productName']
        received_quantity = int(data['receivedQuantity'])
        allocations = data['allocations']  # List of allocations: [{'storeId': 1, 'allocatedQuantity': 50}, ...]

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert the product into the Products table
        cursor.execute(
            "INSERT INTO Products (ProductName, ReceivedQuantity) OUTPUT INSERTED.ProductID VALUES (?, ?)",
            (product_name, received_quantity)
        )
        product_id = cursor.fetchone()[0]  # Get the inserted ProductID

        # Insert the allocations into the StoreInventory table
        for allocation in allocations:
            store_id = allocation['storeId']
            allocated_quantity = allocation['allocatedQuantity']
            cursor.execute(
                "INSERT INTO StoreInventory (StoreID, ProductID, AllocatedQuantity) VALUES (?, ?, ?)",
                (store_id, product_id, allocated_quantity)
            )

        connection.commit()
        return jsonify({'message': 'Inventory updated successfully!'}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

    finally:
        connection.close()


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
