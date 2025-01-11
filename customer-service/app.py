from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Conexión a la base de datos MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            database="CustomerDb",
            user="root",  # Cambia esto si usas otro usuario
            password="pandani09"  # Cambia esto por la contraseña que has configurado
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Endpoint para registrar un cliente
@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.json
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES (%s, %s, %s, %s)",
            (data['FirstName'], data['LastName'], data['Email'], data['PhoneNumber'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Customer created successfully!"}), 201
    return jsonify({"message": "Failed to connect to database"}), 500

# Endpoint para obtener información de un cliente
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        conn.close()
        if customer:
            return jsonify({
                "CustomerID": customer[0],
                "FirstName": customer[1],
                "LastName": customer[2],
                "Email": customer[3],
                "PhoneNumber": customer[4],
                "Address": customer[5],
                "CreatedAt": customer[6],
                "UpdatedAt": customer[7]
            })
        else:
            return jsonify({"message": "Customer not found"}), 404
    return jsonify({"message": "Failed to connect to database"}), 500

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
