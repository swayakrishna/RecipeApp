#Flask Application main 

from flask import Flask, render_template, request, redirect, flash
from models import db, Recipe, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recipe.db"

db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

#global variable to know if user is already logged in or not
authenticated_user = None

#homepage route
@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()  #gets the search query
    if authenticated_user:
        if search_query:
            recipes = Recipe.query.filter(Recipe.title.ilike(f"%{search_query}%")).all()
        else:
            recipes = Recipe.query.all()
        return render_template('index.html', recipes=recipes, search_query=search_query)
    else:
        return redirect('/login')

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
    if request.method == 'POST':   
        recipe.title=request.form['title']
        recipe.ingredients=request.form['ingredients']
        recipe.steps=request.form['steps']
        recipe.difficulty=request.form['difficulty']
        recipe.cooking_time=request.form['cooking_time']
        db.session.commit()
        return redirect('/')
    return render_template('edit_recipe.html', recipe=recipe)

#TODO remove this at last Listing recipes
#This route is working but not being used in the application currently
@app.route('/list_recipe')
def list_recipe():
    recipes = Recipe.query.all()
    if request.method == 'POST':   
        print(Recipe)
    return render_template('list_recipe.html', recipes=recipes)

# Delete recipe route
@app.route('/delete_recipe/<int:recipe_id>')
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_pass = request.form['confirm_password']

        existing_user = User.query.filter_by(username=username).first()
        if not email or not username or not password or not confirm_pass:
            flash('All fields are required.', 'error')
            return redirect(request.url)
        if password != confirm_pass:
            flash('Passwords doesnt match', 'error')
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global authenticated_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Both username and password are required.', 'error')
            return redirect(request.url)
            
        user = User.query.filter_by(username=username).first_or_404()

        if user:
            authenticated_user = username
            return redirect('/')
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    global authenticated_user
    authenticated_user = None
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)