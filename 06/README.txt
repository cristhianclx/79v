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

>>> User.query.all()

>>> item = User(code="104", first_name="Alan", last_name="ABC", age=22)
>>> db.session.add(item)
>>> db.session.commit()

>>> User.query.get_or_404(4)
>>> User.query.filter_by(id=4).first()
>>> User.query.filter_by(first_name="Alan").first()

>>> item = User.query.get_or_404(4)
>>> item.age = 32
>>> db.session.add(item)
>>> db.session.commit()

>>> item = User.query.get_or_404(4)
>>> db.session.delete(item)
>>> db.session.commit()