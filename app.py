from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('films', user='jeffreylu',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Films(BaseModel):
    name = CharField()
    director = CharField()
    release_date = IntegerField()
    rt_score = IntegerField()


db.create_tables([Films])
db.drop_tables([Films])
db.create_tables([Films])

Films(name='Castle in the Sky', director='Hayao Miyazaki',
      release_date='1986', rt_score='95').save()
Films(name='Grave of the Fireflies', director='Isao Takahata',
      release_date='1988', rt_score='97').save()
Films(name='My Neighbor Totoro', director='Hayao Miyazaki',
      release_date='1988', rt_score='93').save()
Films(name='Kiki\'s Delivery Service', director='Hayao Miyazaki',
      release_date='1989', rt_score='96').save()
Films(name='Princess Mononoke', director='Hayao Miyazaki',
      release_date='1997', rt_score='92').save()
Films(name='Spirited Away', director='Hayao Miyazaki',
      release_date='2001', rt_score='97').save()

app = Flask(__name__)


@app.route('/films', methods=['GET', 'POST'])
@app.route('/films/<name>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(name=None):
    if request.method == 'GET':
        if name:
            return jsonify(model_to_dict(Films.get(Films.name == name)))
        else:
            filmList = []
            for name in Films.select():
                filmList.append(model_to_dict(name))
            return jsonify(filmList)

    if request.method == 'PUT':
        data = request.get_json()
        Films.update(data).where(Films.name == name).execute()
        return ("updated")

    if request.method == 'POST':
        name = dict_to_model(Films, request.get_json())
        name.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Films.delete().where(Films.name == name).execute()
        return ("It's been deleted!")


app.run(debug=True, port=9000)
