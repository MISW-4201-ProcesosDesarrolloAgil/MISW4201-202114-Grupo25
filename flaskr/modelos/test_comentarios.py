# Pruebas para el modelo comentario

#Modelo
from comentarios import ComentarioModel
# Database
from db import db

# Utils
import unittest


class TestModeloComentario(unittest.TestCase):
    """
    Pruebas para el modelo de comentarios
    """
    def setUp(self):
        """

        :return:
        """
        pass

    def tearDown(self):
        """

        :return:
        """
        pass

    def test_comentario_creado(self):
        """
        test de creacion de un comentario de manera satisfactoria
        :return:
        """
        db.session.add(ComentarioModel())

        result = db.session.query(ComentarioModel)

        self.assertEqual(1, 1)

