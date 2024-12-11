#Flask Application main 

from flask import Flask, render_template, request
from models import db, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipe.db"

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

#homepage route
@app.route('/')
def index():
    recipes = Recipe.query.all()  # Fetch all recipes from the database
    return render_template('index.html', recipes=recipes)

#adding new recipe route
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title=request.form['title']
        ingredients=request.form['ingredients']
        steps=request.form['steps']
        difficulty=request.form['difficulty']
        cooking_time=request.form['cooking_time']
        print("POST : ",title,ingredients,steps,difficulty,cooking_time)
        print("POST : ",type(title),type(ingredients),type(steps),type(difficulty),type(cooking_time))

        if not title or not ingredients or not steps or not difficulty or not cooking_time:
            flash('All fields are required.', 'error')
        else:
            new_recipe = Recipe(title=title,ingredients=ingredients,steps=steps,difficulty=difficulty,cooking_time=cooking_time)
            db.session.add(new_recipe)
            db.session.commit()
            return redirect('/')

    return render_template('add_recipe.html')

#editing existing recipe app route
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    print(recipe)
    return render_template('edit_recipe.html', recipe=recipe)

#TODO remove this at last Listing recipes
@app.route('/list_recipe')
def list_recipe():
    recipes = Recipe.query.all()
    if request.method == 'POST':   
        print(Recipe)
    return render_template('list_recipe.html', recipes=recipes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)