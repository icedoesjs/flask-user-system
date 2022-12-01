from flask import render_template, request, Blueprint, url_for, redirect, flash
from .forms import CreateUser, LoginForm, PokemonForm
from requests import get
from flask_login import login_user, logout_user, current_user
from app.models import Users
from werkzeug.security import check_password_hash
from datetime import date

auth = Blueprint('auth', __name__, template_folder='auth_templates')
today = date.today()



def getpmInfo(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    res = get(url)
    if res.ok:
        data = res.json()
        return data 
    else:
        return False
    
poke_info = {}
def addtoInfo(name, ability, base_exp, sprite_url, attack_base, hp_base, def_base):
    poke_info["name"] = name.title()
    poke_info["ability"] = ability
    poke_info["base_exp"] = base_exp
    poke_info["front_shiny"] = sprite_url
    poke_info["attack_base"] = attack_base
    poke_info["hp_base"] = hp_base
    poke_info["defense_base"] = def_base

@auth.route('/viewer', methods=['GET', 'POST'])
def viewer():
    form = PokemonForm()
    if request.method == 'POST':
        if form.validate():
            poke_name = form.poke_name.data
            
            data = getpmInfo(poke_name.lower())
            
            if data == False: 
                flash('That pokemon was not found')
            else:
                name = data["name"]
                ability = data["abilities"][1]["ability"]["name"]
                base_exp = data["base_experience"]
                sprite_url = data["sprites"]["front_shiny"]
                attack_base = data["stats"][1]["base_stat"]
                hp_base = data["stats"][0]["base_stat"]
                def_base = data["stats"][2]["base_stat"]
                addtoInfo(name, ability, base_exp, sprite_url, attack_base, hp_base, def_base)
                return render_template('info.html', data=poke_info)
            
    return render_template('viewer.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CreateUser()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data 
            email = form.email.data
            password = form.password.data 
            firstName = form.first_name.data 
            lastName = form.last_name.data 
            date_created = today.strftime("%B %d, %Y")
    
            user = Users(firstName, lastName, username, email, password, date_created)
            
            user.save_to_db()
            return redirect(url_for('auth.login'))
        
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data 
            password = form.password.data 
            
            user = Users.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    print('incorrect password')
            else:
                flash('Cannot find a user with that username')
        
    return render_template('login.html', form=form)
        
@auth.route('/logout')
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))