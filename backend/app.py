from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app)


def get_db_connection():
    connection = psycopg2.connect(
        user='your_username',
        password='your_password',
        host='localhost',
        port='5432',
        database='your_database'
    )
    return connection


@app.route('/api/testcases', methods=['GET'])
def get_test_cases():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM testcases;')
    test_cases = cursor.fetchall()

    result = []
    for test_case in test_cases:
        test_case_data = {
            'id': test_case[0],
            'name': test_case[1],
            'description': test_case[2],
            'estimate_time': test_case[3].total_seconds() if test_case[3] else None,
            'module': test_case[4],
            'priority': test_case[5]
        }
        result.append(test_case_data)

    cursor.close()
    connection.close()

    return jsonify(result)


@app.route('/api/testcases', methods=['POST'])
def create_test_case():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    estimate_time = data.get('estimate_time')
    module = data.get('module')
    priority = data.get('priority')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO testcases (name, description, estimate_time, module, priority) '
        'VALUES (%s, %s, %s, %s, %s) RETURNING id;',
        (name, description, estimate_time, module, priority)
    )
    new_test_case_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    new_test_case_data = {
        'id': new_test_case_id,
        'name': name,
        'description': description,
        'estimate_time': estimate_time.total_seconds() if estimate_time else None,
        'module': module,
        'priority': priority
    }
    socketio.emit('test_case_created', new_test_case_data, broadcast=True)

    return jsonify({'message': 'Test case created successfully'})


if __name__ == '__main__':
    socketio.run(app)
