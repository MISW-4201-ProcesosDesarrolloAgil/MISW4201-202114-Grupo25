# Utils
import json

# Models
from flaskr.modelos import Cancion, Usuario

# unitest
from flaskr.tests.base_case import BaseCase, get_headers, get_access_token


class TestVistaVisualizarCanciones(BaseCase):
    """ TestEjemploVista ejecuta tests de vista xxx """

    def test_visualizar_canciones(self):
        """
        test_visualizar_canciones prueba el caso de una canción que existe y es compartida

        Para esto se toma como referencia que en los datos de prueba cargado, se comparte el album de id2 con el usuario de id1
        """
        token = get_access_token(self.app)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Configuracion: Se comparte la cancion para probar posteriormente
        #self.app.post("cancion/1/usuarios-compartidos", headers=headers,
         #                        data=json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]}))

        endpoint = "/canciones"
        response = self.app.get(endpoint, headers=headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual("Black in Black", response.json[-1].get('titulo'))
        self.assertEqual("AC/DC",response.json[-1].get('interprete'))
        self.assertEqual(2,response.json[-1].get('usuario'))






