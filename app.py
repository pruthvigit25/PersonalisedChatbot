from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import classify
import json
import re
import mysql.connector

app = Flask(__name__)
app.secret_key = 'spaceguru123'  
CORS(app)

db_host = '34.69.76.50'
db_user = 'root'
db_password = 'spaceguruserver'
db_name = 'spaceguru_db'
stored_username_global = None

def create_database_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def fetch_age(username):
        connection = create_database_connection()
        cursor = connection.cursor()
        query = "SELECT age FROM user_table WHERE username = '"+username+"'"
        print(query)
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            age = result[0]
            return age
        else:
            return 0
                
        cursor.close()
        connection.close()

def askOpenai(age, message,storedUsername):
    prompt  = message + ".Respond as if you are telling to a "+age+"years old "

    openai.api_key = "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"
    prompt = prompt
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=100,
        n=1, 
        stop=None,  
    )
    answer = response.choices[0].text.strip()
    table_name = storedUsername+"_qanda"
    insert_query = "INSERT INTO "+table_name+" (username, questions, answers) VALUES (%s, %s, %s)"
    data = (storedUsername, message, answer)

    try:
        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute(insert_query, data)
        connection.commit()
        cursor.close()
        connection.close()
        print("Data inserted successfully!")
    except mysql.connector.Error as err:
        print("Error:", err)
    return answer 

@app.route('/get_stored_username')
def get_stored_username():
    stored_username = request.args.get('stored_username')
    print("PRINTING USER NAME!!!")
    session['stored_username'] = stored_username
    print(session.get('stored_username'))
    return jsonify({'username': stored_username})

@app.route('/callapi')
def hey():
    message = request.args.get('message')
    storedUsername = request.args.get('storedUsername')
    age = str(fetch_age(storedUsername))
    print(message)
    if classify.isSpace(message):
        return askOpenai(age, message,storedUsername)
    else:
            return "Please ask Questions related to Space!"
    
    
@app.route('/suggestions')
def suggestion():
    message = request.args.get('message')
    storedUsername = request.args.get('storedUsername')
    age = str(fetch_age(storedUsername))
    prompt = 'give me 3 more questions related to this question " ' + message + '". Frame the question such as you are suggesting it to '+age+' year old'

    print(prompt)

    openai.api_key = "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"
    prompt = prompt
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=100,
        n=1, 
        stop=None,  
    )
    answer = response.choices[0].text.strip()
    string_without_numbers = re.sub(r'\d+\.', '', answer)
    questions = re.split(r'\?\s', string_without_numbers)
    questions = [question.strip() + '?' for question in questions]

    question_dict = {}
    for i, question in enumerate(questions):
        question_dict[f"{i}"] = question

    json_data = json.dumps(question_dict, indent=4)

    print(json_data)
    return json_data 


@app.route('/registeruser', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print(data)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        age = data.get('age')
        school_college_name = data.get('school_college_name')
        city = data.get('city')
        country = data.get('country')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')

        connection = create_database_connection()
        cursor = connection.cursor()

        insert_query = (
            "INSERT INTO user_table "
            "(first_name, last_name, username, age, school_college_name, city, country, email, password, gender) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(insert_query, (
            first_name, last_name, username, age, school_college_name,
            city, country, email, password, gender
        ))

        create_questions_answers_table_query = """CREATE TABLE """ + username + """_qanda (questions TEXT,answers TEXT,username VARCHAR(255), FOREIGN KEY (username) REFERENCES user_table(username))"""
        print(create_questions_answers_table_query)
        cursor.execute(create_questions_answers_table_query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/usersignin', methods=['POST'])
def user_signin():
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        connection = create_database_connection()
        cursor = connection.cursor()

        select_query = "SELECT COUNT(*) FROM user_table WHERE username = %s AND password = %s"
        cursor.execute(select_query, (username, password))
        result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if result > 0:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 399

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/getreflectionanswers', methods=['POST'])
def get_reflection_answers():
    try:
        data = request.json
        print(data)
        username = data.get('username')
        answer1 = data.get('answer1')
        answer2 = data.get('answer2')
        answer3 = data.get('answer3')
        answer4 = data.get('answer4')
        answer5 = data.get('answer5')

        connection = create_database_connection()

       
        cursor = connection.cursor()

       
        insert_query = "INSERT INTO reflection_answers (username, answer1, answer2, answer3, answer4, answer5) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (username, answer1, answer2, answer3, answer4, answer5))

        
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Survey answers saved successfully'})

    except Exception as e:
        
        connection.rollback()
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True) 
    
