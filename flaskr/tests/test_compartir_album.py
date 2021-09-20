# Utils
import json

#Models
from flaskr.modelos import Album, Usuario

# unitest
from flaskr.tests.base_case import BaseCase, get_headers

class TestVistaAlbumesUsuariosCompartidos(BaseCase):
    """ TestVistaAlbumesUsuariosCompartidos ejecuta tests de vista VistaAlbumesUsuariosCompartidos """

    def test_compartir_satisfactoriamente(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": ["Jacquette", "Cassi"]
        })
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Álbum compartido.", response.json)
    
    def test_valor_id_album_no_soportado(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": ["Lauren"]
        })
        endpoint = "album/9223372036854775808/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("El campo id_album solo permite int como valor.", response.json)

    def test_compartir_album_no_existe(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": ["Lauren"]
        })
        endpoint = "album/21/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual("El álbum no existe", response.json)
    
    def test_compartir_album_de_otro_usuario(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": ["Jacquette", "Cassi"]
        })
        endpoint = "album/2/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Solo el dueño del álbum puede compartirlo.", response.json)

    def test_enviar_lista_usuarios_compartidos(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": "Jacquette, Cassi"
        })
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("El campo usuarios_compartidos solo permite array como valor.", response.json)

    def test_enviar_arreglo_de_usuarios_vacio(self):
        headers = get_headers(self.app)
        payload = json.dumps({
            "usuarios_compartidos": []
        })
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("No hay usuarios para compartir el álbum.", response.json)

    def test_compartir_usuarios_repetidos(self):
        headers = get_headers(self.app)
        payload = json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]})
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        payload = json.dumps({ "usuarios_compartidos":  ["Jacquette", "Cassi"]})
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("No hay usuarios nuevos para compartir el álbum o los que están no pueden ser removidos.", response.json)

    def test_remover_usuarios_compartidos(self):
        headers = get_headers(self.app)
        payload = json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]})
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        payload = json.dumps({"usuarios_compartidos": ["Jacquette"]})
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(409, response.status_code)
        self.assertEqual("Los usuarios compartidos no pueden ser removidos.", response.json)

    def test_compartir_con_usuario_inexistente(self):
        headers = get_headers(self.app)
        payload = json.dumps({"usuarios_compartidos": ["Usuario-inexistente"]})
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual("El usuario: Usuario-inexistente, no existe.", response.json)

    def test_obtener_usuarios_compartidos_valor_id_album_no_soportado(self):
        headers = get_headers(self.app)
        endpoint = "album/9223372036854775808/usuarios-compartidos"
        response = self.app.get(endpoint, headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual("El campo id_album solo permite int como valor.", response.json)

    def test_obtener_usuarios_compartidos_album_no_existe(self):
        headers = get_headers(self.app)
        endpoint = "album/21/usuarios-compartidos"
        response = self.app.get(endpoint, headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertEqual("El álbum no existe.", response.json)
    
    def test_obtener_usuarios_compartidos_de_album_de_otro_usuario(self):
        headers = get_headers(self.app)
        endpoint = "album/2/usuarios-compartidos"
        response = self.app.get(endpoint, headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Solo el dueño del álbum puede ver con quién lo compartió.", response.json)
    
    def test_obtener_usuarios_compartidos(self):
        headers = get_headers(self.app)
        endpoint = "album/1/usuarios-compartidos"
        response = self.app.get(endpoint, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual({'usuarios_compartidos': []}, response.json)

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
