# Utils
import json

# unitest
from flaskr.tests.base_case import BaseCase

# Modelo
from flaskr.tests.base_case import get_access_token


class TestVisualizarAlbumesVista(BaseCase):
    """ TestVisualizarAlbumesVista ejecuta tests de vista VistaAlbumsUsuario """

    def test_consulta_album_propio(self):
        """
        test_consulta_satisfactoria verifica la consulta satisfactoria de un album propio
        """
        token = get_access_token(self.app)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        endpoint = "/albumes"

        response = self.app.get(endpoint, headers=headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual("Urban Menace", response.json[0].get('titulo'))
        self.assertEqual("monetize mission-critical ROI", response.json[0].get('descripcion'))
        self.assertEqual(1, response.json[0].get('usuario'))
        self.assertEqual(1987, response.json[0].get('anio'))
        self.assertEqual([], response.json[0].get('canciones'))

    def test_caso_album_compartido(self):
        """
        test_caso_album_compartido verifica la consulta satisfactoria de un album compartido
        para esto se toma de referencia que en la carga de datos de prueba se comparte el album de id 2 con el usuario de id 1
        """
        token = get_access_token(self.app)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        endpoint = "/albumes"

        response = self.app.get(endpoint, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, response.json[-1].get('usuario'))