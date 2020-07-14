## I - Mesma route para /home e /home/<name>
@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Default'})
@app.route('/home/<name>', methods=['POST', 'GET'])

## II - Queries
@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)

## III - Routes 
$ Eu posso usar o mesmo nome da route 2x, um só pra GET
e outro só pra POST 

# IV - Session
$ Posso criar um dicionario acessavel e guardar em um cookie
$ Assim, ele é acessavel por todo o codigo
$ Precisa nesse caso ser guardado pela secret key
$ Nao posso guardar dados sensiveis nele. Precisa da secret key pra modificar seu conteudo

app.config['SECRET_KEY'] = 'totallysecret'
session['name'] = 'nome'
..
name = session['name']

# V - Debug
$ Posso salvar o Pin-code do Debug e usar na msg de erro.
$ Assim, posso inspecionar as variaveis naquele momento
