# Utils
import json

# unitest
from flaskr.tests.base_case import BaseCase

# Modelo
from flaskr.modelos.comentarios import ComentarioModel
from flaskr.tests.base_case import GetAccessToken

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
        token = GetAccessToken(self.app)

        payload = json.dumps({
            "descripcion": "Test Prueba"
        })

        headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
        }

        response = self.app.post("/album/1/comentario", headers=headers, data=payload)

        self.assertEqual(201, response.status_code)


class TestModeloComentario(BaseCase):
    """
    Tests para el modelo de comentarios
    """

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
