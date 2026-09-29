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
        return {
            "id": raw["name"],
            "height": raw["height"],
            "weight": raw["weight"],
            "abilities": [], # ["limber", "imposter", "..."]
            "forms": [], # ["ditto"]
        }


api.add_resource(HelloWorldResource, '/')
api.add_resource(PokemonByNameResource, '/by-name/<name>')


# LABORATORIO
# incluir abilities y forms en la respuesta
# http://127.0.0.1:5000/by-name/pikachu