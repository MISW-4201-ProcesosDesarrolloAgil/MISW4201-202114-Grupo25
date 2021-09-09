# tests
import unittest
from flaskr.tests.data import seed_data

# Flask
from flaskr.app import app
from flaskr.modelos.database import db

# Utils
import json

class BaseCase(unittest.TestCase):
    """
    BaseCase es el caso base para todos los tests.

    Se debe heredar de esta clase al generar un nuevo test
    """

    def setUp(self):
        """
        setUp configura la aplicacion y base de datos
        """
        self.app = app.test_client()
        self.db = db
        self.db.create_all()
        seed_data(self.db)

    def tearDown(self):
        """
        tearDown elimina la sesion y borra la base de datos
        """
        self.db.session.remove()
        self.db.drop_all()


def GetAccessToken(application):
    """
    getAccessToken
    """
    payload = json.dumps({  # Data from seed method
        "nombre": "Enrique",
        "contrasena": "H0zksFgA8k6"
    })
    response = application.post("/logIn", headers={"Content-Type": "application/json"}, data=payload)
    return response.json.get('token')


