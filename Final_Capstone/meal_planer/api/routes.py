from flask import Blueprint, request, jsonify
from meal_planer.models import db

api = Blueprint('api', __name__, url_prefix='/api')



API_KEY = 'YOUR_SPOONACULAR_API_KEY'

def get_meal_data():
    url = 'https://api.spoonacular.com/recipes/random'
    params = {
        'apiKey':"e1794d5396a64d5e8a4767fe05db9565",
        'number': 3,  # Adjust the number of meals you want to retrieve
    }
    response = request.get(url, params=params)
    if response.ok:
        return response.json().get('recipes', [])
    return []