# Utils
import json

# Models
from flaskr.modelos import Cancion, Usuario

# unitest
from flaskr.tests.base_case import BaseCase, get_headers, get_access_token


class TestVistaVisualizarCanciones(BaseCase):  # Siempre se debe heredar de BaseCase
    """ TestEjemploVista ejecuta tests de vista xxx """

    def test_visualizar_canciones(self):
        """
        test_caso_1 prueba el caso de una canción que existe y es compartida
        """
        token = get_access_token(self.app)  # Aplica unicamente para endpoints protegidos con jwt

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"  # Aplica unicamente a endpoints protegidos con jwt
        }

        # Configuracion: Se comparte la cancion para probar posteriormente
        response = self.app.post("cancion/1/usuarios-compartidos", headers=headers,
                                 data=json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]}))

        endpoint = "/canciones"  # Reemplazar por endpoint a probar
        response = self.app.get(endpoint, headers=headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response[0].get('titulo'), "Urban Menace")
        self.assertEqual(response[0].get('anio'), 1987)
        self.assertEqual(response[0].get('descripcion'),"monetize mission-critical ROI")
        self.assertEqual(response[0].get('usuario'), 1)

    #def test_visualizar_canciones_no_existe(self):






