from flaskr import create_app
from .modelos import Cancion, Usuario
from flaskr.modelos.database import db
import unittest
from flaskr.tests.data import seed_data

class TestModelos(unittest.TestCase):

    def create_app(self):
        self.app = create_app('default', 'sqlite:///test.db')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def setUp(self):
        self.create_app()
        db.init_app(self.app)
        db.create_all()
        seed_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_crear_cancion(self):
        result = db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "titulo")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "interprete")
        self.assertEqual(result[0].usuario, 1)
    
    def test_compartir_cancion_con_duenio(self):
        excepcion_obtenida = None
        usuarios = result = db.session.query(Usuario)
        canciones = db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[0])
        try:
            canciones[0].usuarios_compartidos = usuarios_compartidos
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)

    def test_compartir_cancion_con_usuario(self):
        usuarios = result = db.session.query(Usuario)
        canciones = db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        canciones[0].usuarios_compartidos = usuarios_compartidos
        db.session.commit()

        result = db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "titulo")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "interprete")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_cancion_con_usuarios_y_duenio(self):
        usuarios = result = db.session.query(Usuario)
        canciones = db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[2])
        usuarios_compartidos.append(usuarios[0])
        try:
            canciones[0].usuarios_compartidos = usuarios_compartidos
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)
    
    def test_compartir_cancion_con_usuarios(self):
        usuarios = result = db.session.query(Usuario)
        canciones = db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[2])
        usuarios_compartidos.append(usuarios[3])
        usuarios_compartidos.append(usuarios[4])
        usuarios_compartidos.append(usuarios[5])
        usuarios_compartidos.append(usuarios[6])
        usuarios_compartidos.append(usuarios[7])
        usuarios_compartidos.append(usuarios[8])
        canciones[0].usuarios_compartidos = usuarios_compartidos
        db.session.commit()

        result = db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "titulo")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "interprete")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_cancion_con_usuario_repetido(self):
        usuarios = result = db.session.query(Usuario)
        canciones = db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[1])
        try:
            canciones[0].usuarios_compartidos = usuarios_compartidos
            db.session.commit()
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)