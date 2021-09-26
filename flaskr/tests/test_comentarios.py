# Utils
import json
from datetime import datetime

# unitest
from flaskr.tests.base_case import BaseCase, get_headers

# Modelo
from flaskr.modelos.comentarios import ComentarioModel, ComentarioSchema
# Database
from flaskr.modelos.database import db

comentario_schema = ComentarioSchema()

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
            "descripcion": "*" * 1001,
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)
        self.assertEqual(400, response.status_code, "invalid response code")
        self.assertEqual("el comentario no puede tener mas de 1000 caracteres", response.json.get('message'))

        # Case 2
        payload = json.dumps({
            "descripcion": "*" * 1000,
        })
        response = self.app.post("/album/1/comentario", headers=headers, data=payload)

        self.assertEqual(201, response.status_code, "respuesta ok")
        self.assertEqual("comentario creado satisfactoriamente", response.json.get('message'))

    def test_consultar_comentarios(self):
        """ Test consultar comentarios en orden descendente"""
        headers = get_headers(self.app)

        response = self.app.get("/album/1/comentario", headers=headers)

        self.assertEqual(200, response.status_code, "invalid response code")
        # self.assertEqual(expected, response.json, "invalid response")

        # Descripcion de comentarios
        self.assertEqual(response.json[0].get('descripcion'), "Comentario de prueba numero 4")
        self.assertEqual(response.json[1].get('descripcion'), "Comentario de prueba numero 3")
        self.assertEqual(response.json[2].get('descripcion'), "Comentario de prueba numero 2")
        self.assertEqual(response.json[3].get('descripcion'), "Comentario de prueba numero 1")

        # Id de comentario
        self.assertEqual(response.json[0].get('id'), 4)
        self.assertEqual(response.json[1].get('id'), 3)
        self.assertEqual(response.json[2].get('id'), 2)
        self.assertEqual(response.json[3].get('id'), 1)

        # Usuario relacionado con el comentario
        self.assertEqual(response.json[0].get('user').get('nombre'), "Jacquette")
        self.assertEqual(response.json[1].get('user').get('nombre'), "Jacquette")
        self.assertEqual(response.json[2].get('user').get('nombre'), "Enrique")
        self.assertEqual(response.json[3].get('user').get('nombre'), "Enrique")

        # Fechas de creacion
        fechas_comentarios = []
        for fecha in response.json:
            fecha_str = fecha.get('fecha_creacion').replace("T", " ")
            fechas_comentarios.append(datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f"))
        self.assertGreater(fechas_comentarios[0], fechas_comentarios[1])
        self.assertGreater(fechas_comentarios[1], fechas_comentarios[2])
        self.assertGreater(fechas_comentarios[2], fechas_comentarios[3])


class TestModeloComentario(BaseCase):
    """ Tests para el modelo de comentarios """

    def test_crear_comentario_correcto(self):
        """
        test de creacion de un comentario de manera satisfactoria
        :return:
        """
        descripcion = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae cursus nibh. Donec " \
                      "elementum at. "
        self.db.session.add(ComentarioModel(id=100, descripcion=descripcion))
        self.db.session.commit()

        result = db.session.query(ComentarioModel).filter_by(id=100)

        self.assertEqual(result[0].id, 100)
        self.assertEqual(result[0].descripcion, descripcion)

    def test_crear_comentario_vacio(self):
        """
        test de creacion de un comentario vacio
        :return:
        """
        descripcion = ""
        try:
            self.db.session.add(ComentarioModel(id=2, descripcion=descripcion))
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_consultar_comentarios_de_album(self):
        "test para consultar un comentario por album"
        result = ComentarioModel.get_by_album(1)

        # Descripcion de comentarios
        self.assertEqual(result[0].descripcion, "Comentario de prueba numero 4")
        self.assertEqual(result[1].descripcion, "Comentario de prueba numero 3")
        self.assertEqual(result[2].descripcion, "Comentario de prueba numero 2")
        self.assertEqual(result[3].descripcion, "Comentario de prueba numero 1")

        # Id de comentario
        self.assertEqual(result[0].id, 4)
        self.assertEqual(result[1].id, 3)
        self.assertEqual(result[2].id, 2)
        self.assertEqual(result[3].id, 1)

        # Usuario relacionado con el comentario
        self.assertEqual(result[0].user.nombre, "Jacquette")
        self.assertEqual(result[1].user.nombre, "Jacquette")
        self.assertEqual(result[2].user.nombre, "Enrique")
        self.assertEqual(result[3].user.nombre, "Enrique")

        # Fechas de creacion
        self.assertGreater(result[0].fecha_creacion, result[1].fecha_creacion)
        self.assertGreater(result[1].fecha_creacion, result[2].fecha_creacion)
        self.assertGreater(result[2].fecha_creacion, result[3].fecha_creacion)

