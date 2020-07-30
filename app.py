from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import requests, json
import datetime

app =  Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Thisisasecret"

@app.route('/')
def index():

    url = "http://127.0.0.1:5050/frage"
    response = requests.get(url)
    frage = json.loads(response.content)

    message = frage['frage']
    pattern = frage['num_frage']

    print(frage)

    session['chat'] = []

    date = datetime.datetime.now()
    date = date.strftime("%c")

    session['current_frage'] = frage

    chat = {"date": date, "sender": "robot", "message": message}
    session['chat'].append(chat)

    return render_template("test.html", chat=session['chat'])

    #return render_template("index.html", frage=frage)

@app.route('/', methods=['POST'])
def submit():

    data = {
        'num_frage': session['current_frage']['num_frage'],
        'antwort': request.form['antwort']}

    date = datetime.datetime.now()
    chat = {"date": date, "sender": "user", "message": data['antwort']}
    session['chat'].append(chat)

    print(f'data={data}')

    url = "http://127.0.0.1:5050/frage"

    response = requests.post(url, json=data)
    response = json.loads(response.content)

    date = datetime.datetime.now()
    if response['success']:
        
        message = response['bot_antwort']['result']
        pattern = response['bot_antwort']['context']
        chat = {"date": date, "sender": "robot", "message": message}
        session['chat'].append(chat)

        frage = {'num_frage': pattern, 'frage': message}
        session['current_frage'] = frage
    else:
        for error in response['errors']:
            message = f"{error['match']}\n{error['tip']}"
            chat = {"date": date, "sender": "gerbot", "message": message}
            session['chat'].append(chat)
            print(f"Found error: {message}") 
        frage = session['current_frage']


    return render_template("test.html", chat=session['chat'])

    #return render_template('index.html', response=response, frage=frage)

if __name__ == '__main__':
    app.run(port=5070)