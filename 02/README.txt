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