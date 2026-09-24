# entorno virtual
python -m venv venv # solo si no tienes la carpeta venv

# activar el entorno virtual
.\venv\Scripts\Activate.ps1
.\venv\Scripts\Activate.bat
# (venv) deberia salir activado

# instalar paquetes
pip install -r requirements.txt
pip install -r requirements.txt --upgrade

# instalar 1 paquete
pip install Flask

# ver los paquetes instalados
pip freeze

# desactiva el entorno virtual
deactivate

# donde descargar python
https://www.python.org/downloads/

#
.\venv\Scripts\Activate.ps1
flask --app main run --reload



# no es necesario para los laboratorios
# https://docs.github.com/en/get-started/using-github/hello-world
git init
git add .
git commit -m "01"
git push origin main