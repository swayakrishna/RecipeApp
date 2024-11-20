#Flask Application main 

from flask import Flask, render_template
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipe.db"

db.init_app(app)

#homepage route
@app.route('/')
def index():
    return render_template('index.html')

#adding new recipe route
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        print("POST")
    return render_template('add_recipe.html')

#editing existing app route
@app.route('/edit_recipe')
def edit_recipe():
    return render_template('edit_recipe.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)