from flask import Flask

app = Flask(__name__)

from flask import render_template
from swapi_wrapper import get_person_info

@app.route('/')
def root():
    return 'Hi'

@app.route('/snowmap')
def map():
    return '<h2>Here is a map of Paris in very deep snow</h2>'

@app.route('/about')
@app.route('/info')
def about():
    return 'asdsdgsdf'

@app.route('/greet')
@app.route('/greet/<person>/')
@app.route('/greet/<person>/<surname>')
def greet(person=None, surname=None):
    if person:
        if surname:
            return f'<h3>Greetings {person} {surname}</h3>'
        else:
            return f'<h3>Greetings {person}</h3>'
    else:
        person = 'default'
        return f'<h3>Greetings {person}</h3>'

@app.route('/menu')
def manu():
    link1 = '<a href={}>{}</a>'.format('/', 'Home')
    link2 = '<a href={}>{}</a>'.format('/about', 'About')
    link3 = '<a href={}>{}</a>'.format('/greet', 'Greet')
    link4 = '<a href={}>{}</a>'.format('/snowmap', 'Map')
    
    return f'{link1} | {link2} | {link3} | {link4}'

@app.route('/lunch')
@app.route('/lunch/<dessert>')
def lunch(dessert=None):
    return render_template('lunch.html', dessert=dessert)

@app.route('/person/1')
def person():
    return get_person_info()

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)