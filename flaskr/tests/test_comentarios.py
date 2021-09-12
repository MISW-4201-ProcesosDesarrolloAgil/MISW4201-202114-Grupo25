# Utils
import json

# unitest
from flaskr.tests.base_case import BaseCase, get_headers

# Modelo
from flaskr.modelos.comentarios import ComentarioModel

# Database
from flaskr.modelos.database import db


class TestVistaComentarios(BaseCase):
    """
    Tests para Vista de Comentarios
    """

    def test_creacion_satisfactoria(self):
        """
        test creacion satisfactoria prueba la creacion de un comentario satisfactoriamente
        """
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "descripcion": "Test Prueba"
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual("comentario creado satisfactoriamente", response.json.get('message'))

        # Case 2 - Special Characters
        payload = json.dumps({
            "descripcion": "@#$½&__.?'+ççç\\/"
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual("comentario creado satisfactoriamente", response.json.get('message'))

    def test_comentario_vacio(self):
        """ Test para verificar la validacion de un comentario vacio """
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "descripcion": "    "
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)
        self.assertEqual(400, response.status_code, "invalid response code")
        self.assertEqual("la descripcion no puede estar en blanco", response.json.get('message'))

        # Case 2
        payload = json.dumps({
            "descripcion": ""
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)

        self.assertEqual(400, response.status_code, "invalid response code")
        self.assertEqual("la descripcion no puede estar en blanco", response.json.get('message'))

    def test_comentario_caracteres_excedidos(self):
        """ Test para verificar la validacion del limite maximo de caracteres"""
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "descripcion": "*"*1001,
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)
        self.assertEqual(400, response.status_code, "invalid response code")
        self.assertEqual("el comentario no puede tener mas de 1000 caracteres", response.json.get('message'))

        # Case 2
        payload = json.dumps({
            "descripcion": "*"*1000,
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)

        self.assertEqual(201, response.status_code, "respuesta ok")
        self.assertEqual("comentario creado satisfactoriamente", response.json.get('message'))


class TestModeloComentario(BaseCase):
    """ Tests para el modelo de comentarios """

    def test_comentario_correcto(self):
        """
        test de creacion de un comentario de manera satisfactoria
        :return:
        """
        descripcion = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae cursus nibh. Donec " \
                      "elementum at. "
        self.db.session.add(ComentarioModel(id=1, descripcion=descripcion))
        self.db.session.commit()

        result = db.session.query(ComentarioModel)

        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].descripcion, descripcion)

    def test_comentario_vacio(self):
        """
        test de creacion de un comentario vacio
        :return:
        """
        descripcion = ""
        try:
            self.db.session.add(ComentarioModel(id=2, descripcion=descripcion))
        except Exception as e:
            self.assertIsInstance(e, ValueError)
