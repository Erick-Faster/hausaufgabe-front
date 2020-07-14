from flask import Flask, jsonify, request, url_for, redirect, session, render_template
import requests, json
app =  Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Thisisasecret"

@app.route('/')
def index():

    url = "http://127.0.0.1:5050/frage"
    response = requests.get(url)
    frage = json.loads(response.content)

    session['num_frage'] = frage["num_frage"]

    return render_template("index.html", frage=frage)

@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return render_template('home.html', name=name, display=False, mylist=['one', 'two', 'three', 'four'], listofdictionaries = [{'name': 'Erick'}, {'name':'Mateus'}])

#http://127.0.0.1:5050/query?name=sara&location=morroco
@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

@app.route('/theform')
def theform():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def submit():

    data = {
        'num_frage': session['num_frage'],
        'antwort': request.form['antwort']}

    url = "http://127.0.0.1:5050/frage"

    response = requests.post(url, json=data)

    correction = json.loads(response.content)

    response = requests.get(url)
    frage = json.loads(response.content)

    session['num_frage'] = frage["num_frage"]

    return render_template('index.html', correction=correction, frage=frage)

@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result': 'Success', 'name':name, 'location':location, 'randomkeyinlist':randomlist[1] })

if __name__ == '__main__':
    app.run(port=5070)