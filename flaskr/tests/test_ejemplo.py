# Utils
import json

# unitest
from flaskr.tests.base_case import BaseCase

# Modelo
from flaskr.tests.base_case import GetAccessToken


class TestEjemploVista(BaseCase):  # Siempre se debe heredar de BaseCase para configucara
    """
    TestEjemploVista ejecuta tests de vista xxx
    """

    def test_caso_1(self):
        """
        test_caso_1 prueba el caso 1
        """
        token = GetAccessToken(self.app)  # Aplica unicamente para endpoints protegidos con jwt

        payload = json.dumps({
            "descripcion": "bar"  # Reemplazar por payload a probar
        })

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"  # Aplica unicamente a endpoints protegidos con jwt
        }

        endpoint = "/album/1/comentario"  # Reemplazar por endpoint a probar

        response = self.app.post(endpoint, headers=headers, data=payload)

        self.assertEqual(201, response.status_code)

    def test_caso_2(self):
        """
        test_caso_1 prueba el caso 1
        """
        pass  # ToDo


class TestEjemploModelo(BaseCase):  # Siempre se debe heredar de base case
    """
    TestEjemploModelo ejecuta tests de modelo xxx
    """

    def test_caso_1(self):
        """
        test_caso_1 prueba el caso 1
        :return:
        """
        pass  # Ver ejemplo en archivo test_comentario.py

    def test_caso_2(self):
        """
        test_caso_2 prueba el caso 2
        :return:
        """
        pass
