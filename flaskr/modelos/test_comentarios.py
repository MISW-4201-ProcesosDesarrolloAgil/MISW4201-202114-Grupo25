# Pruebas para el modelo comentario

# Applicacion
from flaskr import create_app

# Modelo
from flaskr.modelos.comentarios import ComentarioModel

# Database
from flaskr.modelos.database import db

# Utils
import unittest


class TestModeloComentario(unittest.TestCase):
    """
    Pruebas para el modelo de comentarios
    """
    def create_app(self):
        """
        creacion de aplicacion de pruebas
        """
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def setUp(self):
        """
        Configuracion de la base de datos
        """
        self.create_app()
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        """
        Limpia ambiente de pruebas
        """
        db.session.remove()
        db.drop_all()

    def test_comentario_correcto(self):
        """
        test de creacion de un comentario de manera satisfactoria
        :return:
        """

        descripcion = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae cursus nibh. Donec elementum at."
        db.session.add(ComentarioModel(id=1, descripcion=descripcion))
        db.session.commit()
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
            db.session.add(ComentarioModel(id=2, descripcion=descripcion))
        except Exception as e:
            self.assertIsInstance(e, ValueError)