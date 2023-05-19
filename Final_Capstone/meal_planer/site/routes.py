from flask import Blueprint, render_template, session, redirect, url_for
from meal_planer.models import MealPlan
site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print("ooga booga in the terminal")
    return render_template('index.html')


@site.route('/dashboard')
def dashboard():
   
    return render_template('profile.html')
   