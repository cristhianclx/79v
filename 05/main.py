from flask import Flask
from flask_restful import Resource, Api
import requests


app = Flask(__name__)
api = Api(app)


class HelloWorldResource(Resource):
    def get(self):
        return {'hello': 'world'}


class PokemonByNameResource(Resource):
    def get(self, name):
        data = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        raw = data.json()
        new_abilities = []
        for x in raw["abilities"]:
            new_abilities.append(x["ability"]["name"])
        new_forms = []
        for x in raw["forms"]:
            new_forms.append(x["name"])
        return {
            "id": raw["name"],
            "height": raw["height"],
            "weight": raw["weight"],
            "abilities": new_abilities,
            "forms": new_forms,
        }


api.add_resource(HelloWorldResource, '/')
api.add_resource(PokemonByNameResource, '/by-name/<name>')