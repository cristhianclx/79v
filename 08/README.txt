# entorno virtual
python -m venv venv # solo si no tienes la carpeta venv

# activar el entorno virtual
.\venv\Scripts\Activate.ps1
.\venv\Scripts\Activate.bat
# (venv) deberia salir activado

# instalar paquetes
pip install -r requirements.txt
pip install -r requirements.txt --upgrade

#
.\venv\Scripts\Activate.ps1
flask --app main run --reload

#
flask --app main db init  # first time
flask --app main db migrate  # create migration
flask --app main db upgrade  # apply migration

flask --app main shell

>>> from main import db, Joke
>>> import pandas as pd
>>> df = pd.read_csv("jokes.csv")
>>> for index, row in df.iterrows():
>>>     item = Joke(routine_id=row["routine_id"], show_id=row["show_id"], event_name=row["event_name"], show_name=row["show_name"], start_timestamp=row["start_timestamp"], text=row["text"], video_id=row["video_id"])
>>>     db.session.add(item)
>>> 
>>> db.session.commit()


# ngrok
# ngrok config add-authtoken xxx
# ngrok http 5000

# https://devcenter.heroku.com/articles/heroku-cli
# heroku login
#   .python-version
#   Procfile
# heroku create