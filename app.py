#Flask Application main 

from flask import Flask, render_template

app = Flask(__name__)

#homepage route
@app.route('/')
def index():
    return render_template('index.html')

#adding new recipe route
@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html')

#editing existing app route
@app.route('/edit_recipe')
def edit_recipe():
    return render_template('edit_recipe.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)