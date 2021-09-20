# Utils
import json

#Models
from flaskr.modelos import Album, Usuario

# unitest
from flaskr.tests.base_case import BaseCase

class TestModelosCompartirAlbum(BaseCase):
    """
    TestModelosCompartirAlbum ejecuta tests de modelo Album
    """

    def test_crear_album(self):
        result = self.db.session.query(Album)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Urban Menace")
        self.assertEqual(result[0].anio, 1987)
        self.assertEqual(result[0].descripcion, "monetize mission-critical ROI")
        self.assertEqual(result[0].usuario, 1)

    def test_compartir_album_con_duenio(self):
        excepcion_obtenida = None
        usuarios = self.db.session.query(Usuario)
        albumes = self.db.session.query(Album)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[0])
        try:
            albumes[0].usuarios_compartidos = usuarios_compartidos
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)

    def test_compartir_album_con_usuario(self):
        usuarios = self.db.session.query(Usuario)
        albumes = self.db.session.query(Album)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        albumes[0].usuarios_compartidos = usuarios_compartidos
        self.db.session.commit()

        result = self.db.session.query(Album)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Urban Menace")
        self.assertEqual(result[0].anio, 1987)
        self.assertEqual(result[0].descripcion, "monetize mission-critical ROI")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_album_con_usuarios_y_duenio(self):
        usuarios = self.db.session.query(Usuario)
        albumes = self.db.session.query(Album)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[2])
        usuarios_compartidos.append(usuarios[0])
        try:
            albumes[0].usuarios_compartidos = usuarios_compartidos
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)

    def test_compartir_album_con_usuarios(self):
        usuarios = self.db.session.query(Usuario)
        albumes = self.db.session.query(Album)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[2])
        usuarios_compartidos.append(usuarios[3])
        usuarios_compartidos.append(usuarios[4])
        usuarios_compartidos.append(usuarios[5])
        usuarios_compartidos.append(usuarios[6])
        usuarios_compartidos.append(usuarios[7])
        usuarios_compartidos.append(usuarios[8])
        albumes[0].usuarios_compartidos = usuarios_compartidos
        self.db.session.commit()

        result = self.db.session.query(Album)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Urban Menace")
        self.assertEqual(result[0].anio, 1987)
        self.assertEqual(result[0].descripcion, "monetize mission-critical ROI")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_album_con_usuario_repetido(self):
        usuarios = self.db.session.query(Usuario)
        albumes = self.db.session.query(Album)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[1])
        try:
            albumes[0].usuarios_compartidos = usuarios_compartidos
            self.db.session.commit()
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)
