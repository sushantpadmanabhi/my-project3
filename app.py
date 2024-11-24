from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/update-inventory')
def update_inventory():
    return send_from_directory('.', 'update-inventory.html')

@app.route('/check-inventory')
def check_inventory():
    return send_from_directory('.', 'check-inventory.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
