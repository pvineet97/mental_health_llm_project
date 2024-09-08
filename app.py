from flask import Flask, request, jsonify
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS on the entire app
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Database connection details
# DB_HOST = "localhost"
# DB_PORT = "5455"
# DB_NAME = "postgres"
# DB_USER = "postgres"
# DB_PASS = "u_pick_password"

def get_db_connection():
    print(os.getenv('DATABASE_URL'))
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM public.user_detail;')  # Assuming you have a 'user_detail' table
    column_names = [desc[0] for desc in cur.description]
    print(column_names)
    users = cur.fetchall()
    
    # Format the result with column names
    result = []
    for row in users:
        row_dict = dict(zip(column_names, row))
        result.append(row_dict)
    
    cur.close()
    conn.close()
    
    return jsonify(result)  # Return the formatted result

@app.route('/login/<user_id>/<password>', methods=['GET'])
def login(user_id,password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM public.user_detail where user_id='{user_id}' and password='{password}';")  # Assuming you have a 'user_detail' table
    users = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return 'True' if users else 'False' , 200 # Return the formatted result

@app.route('/check_user_id_exists', methods=['POST'])
def check_user_id_exists():
    new_user = request.json
    user_id=new_user['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT 'true' FROM user_detail WHERE user_id='{user_id}';")  # Assuming you have a 'user_detail' table
    result = cur.fetchall()
    cur.close()
    conn.close()
    
    return ['True' if result else 'False'], 201

@app.route('/insert_new_user_data', methods=['POST'])
def create_user():
    try:
        new_user = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user_detail (user_id,name, Gender, Age, password, email_id) VALUES (%s,%s, %s, %s, %s, %s)",
                    (new_user['user_id'],new_user['name'], new_user['gender'], new_user['age'], new_user['password'], new_user['email_id']))
        conn.commit()
        cur.close()
        conn.close()
    
        return jsonify(new_user), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()

        if 'duplicate key value violates unique constraint' in str(e):
            return jsonify({'error': 'User with this email_id already exists'}), 400
        else:
            return jsonify({'error': str(e)}), 500
    
@app.route('/insert_pyschometry_data', methods=['POST'])
def insert_pyschometry_response():
    try:
        psychometry_response = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        for i in psychometry_response:
            cur.execute("""INSERT INTO psychometry_response (USER_ID, Question, Response) VALUES (%s, %s, %s)""", 
                    (i['user_id'], i['question'], i['response']))
            conn.commit()
        cur.close()
        conn.close()
    
        return jsonify(psychometry_response), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()
        print(e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_pyschometry_data', methods=['GET'])
def get_pyschometry_data():
    user_id = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    id = user_id['user_id']
    cur.execute(f"SELECT * FROM psychometry_response where user_id='{id}';")  # Assuming you have a 'user_detail' table
    column_names = [desc[0] for desc in cur.description]
    print(column_names)
    users = cur.fetchall()
    
    # Format the result with column names
    result = []
    for row in users:
        row_dict = dict(zip(column_names, row))
        result.append(row_dict)
    
    cur.close()
    conn.close()
    if users:
        return jsonify(result)  # Return the formatted result
    else:
        return f"No pyschometry data found for the user 'user_id'", 201
    
@app.route('/insert_user_activity', methods=['POST'])
def insert_user_activity():
    try:
        new_activity = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert into user_activity
        cur.execute("""
            INSERT INTO user_activity (user_id, session_start_date, session_end_date)
            VALUES (%s, %s, %s)
        """, (new_activity['user_id'], new_activity['session_start_date'], new_activity['session_end_date']))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(new_activity), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()
        print(e)

        if 'duplicate key value violates unique constraint' in str(e):
            return jsonify({'error': 'Duplicate key value error'}), 400
        else:
            return jsonify({'error': str(e)}), 500

@app.route('/insert_emotions_spider_chart', methods=['POST'])
def insert_emotions_spider_chart():
    try:
        new_emotion_data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert into emotions_spider_chart
        cur.execute("""
            INSERT INTO emotions_spider_chart (session_id, happiness, sadness, disgust, love, stress)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (new_emotion_data['session_id'], new_emotion_data['happiness'], new_emotion_data['sadness'],
              new_emotion_data['disgust'], new_emotion_data['love'], new_emotion_data['stress']))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(new_emotion_data), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()

        if 'foreign key violation' in str(e):
            return jsonify({'error': 'Session ID does not exist in user_activity'}), 400
        else:
            return jsonify({'error': str(e)}), 500

@app.route('/insert_session_summary', methods=['POST'])
def insert_session_summary():
    try:
        new_summary = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert into SESSION_Summary
        cur.execute("""
            INSERT INTO SESSION_Summary (session_id, Summary)
            VALUES (%s, %s)
        """, (new_summary['session_id'], new_summary['summary']))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(new_summary), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()

        if 'foreign key violation' in str(e):
            return jsonify({'error': 'Session ID does not exist in user_activity'}), 400
        else:
            return jsonify({'error': str(e)}), 500

@app.route('/insert_chat_history', methods=['POST'])
def insert_chat_history():
    try:
        new_chat = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert into Chat_history
        cur.execute("""
            INSERT INTO Chat_history (session_id, user_text, model_response, time)
            VALUES (%s, %s, %s, %s)
        """, (new_chat['session_id'], new_chat['user_text'], new_chat['model_response'], new_chat['time']))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(new_chat), 201
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of error
        cur.close()
        conn.close()

        if 'foreign key violation' in str(e):
            return jsonify({'error': 'Session ID does not exist in user_activity'}), 400
        else:
            return jsonify({'error': str(e)}), 500

@app.route('/get_sessions_for_user', methods=['GET'])
def get_present_session_id_for_user():
    user_id = request.json
    user_id= user_id["user_id"]
    
    if not user_id:
        return jsonify({'error': 'Missing required parameter: user_id'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to fetch session_id for the given user_id
        cur.execute("""
            SELECT session_id
            FROM user_activity
            WHERE user_id = %s order by session_start_date desc limit 1
        """, (user_id,))
        
        sessions = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert list of tuples to list of session IDs
        session_ids = sessions[0]
        print(sessions[0])
        
        return jsonify({'user_id': user_id, 'session_ids': session_ids}), 200
    
    except Exception as e:
        return jsonify({'error': 'Database error occurred', 'details': str(e)}), 500

@app.route('/get_user_activity/<user_id>', methods=['GET'])
def get_user_activity(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to fetch user activities
        cur.execute("""
            SELECT * FROM user_activity WHERE user_id = %s
        """, (user_id,))
        activities = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        result = [dict(zip(column_names, row)) for row in activities]
        
        cur.close()
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_emotions_spider_chart/<int:session_id>', methods=['GET'])
def get_emotions_spider_chart(session_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to fetch emotions data
        cur.execute("""
            SELECT * FROM emotions_spider_chart WHERE session_id = %s
        """, (session_id,))
        emotions = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        result = [dict(zip(column_names, row)) for row in emotions]
        
        cur.close()
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_session_summary/<int:session_id>', methods=['GET'])
def get_session_summary(session_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to fetch session summary
        cur.execute("""
            SELECT * FROM SESSION_Summary WHERE session_id = %s
        """, (session_id,))
        summaries = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        result = [dict(zip(column_names, row)) for row in summaries]
        
        cur.close()
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/get_chat_history/<int:session_id>', methods=['GET'])
def get_chat_history(session_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        print("1")
        # Query to fetch chat history
        cur.execute("""
            SELECT * FROM Chat_history WHERE session_id = %s
        """, (session_id,))
        chats = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        result = [dict(zip(column_names, row)) for row in chats]
        
        cur.close()
        conn.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def home():
    return jsonify({"message": "API is up and running!"})


if __name__ == '__main__':
    print("Starting Flask App...")
    app.run(debug=True, host='0.0.0.0')
