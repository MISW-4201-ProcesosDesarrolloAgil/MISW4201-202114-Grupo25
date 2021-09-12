# Utils
import json

#Models
from flaskr.modelos import Cancion, Usuario

# unitest
from flaskr.tests.base_case import BaseCase, get_headers


class TestVistaCancionesUsuariosCompartidos(BaseCase):
    """ TestVVistaCancionesUsuariosCompartidos ejecuta tests de vista VistaCancionesUsuariosCompartidos """

    def test_compartir_satisfactoriamente(self):
        """ Test que valida la accion de compartir una cancion satisfactoriamente"""
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "usuarios_compartidos": ["Jacquette", "Cassi"]
        })
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Canción compartida.", response.json)

    def test_compartir_cancion_no_existe(self):
        """
        test_compartir_cancion_no_existe prueba el caso de compartir una cancion que no existe
        """
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "usuarios_compartidos": ["Lauren"]
        })
        endpoint = "cancion/3/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual("La canción no existe", response.json)

    def test_compartir_otro_usuario(self):
        """ Test que valida el caso de compartir una cancion que no le pertenece al usuario"""
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "usuarios_compartidos": ["Jacquette", "Cassi"]
        })
        endpoint = "cancion/2/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("Solo el dueño de la canción puede compartirla.", response.json)

    def test_lista_usuarios_compartidos(self):
        """ Test que valida que los usuarios a compartir sean pasados en una lista"""
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "usuarios_compartidos": "Jacquette, Cassi"
        })
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("El campo usuarios_compartidos solo permite array como valor.", response.json)

    def test_lista_usuarios_vacia(self):
        """ Test que valida que la lista de usuarios a compartir no este vacia"""
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({
            "usuarios_compartidos": []
        })
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("No hay usuarios para compartir la canción.", response.json)

    def test_no_hay_usuarios_nuevos(self):
        """ Test que valida que la lista de usuarios a compartir no tenga usuarios nuevos"""
        # Config
        headers = get_headers(self.app)
        payload = json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]})
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)

        # Case 1
        payload = json.dumps({ "usuarios_compartidos":  ["Jacquette", "Cassi"]})
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(400, response.status_code)
        self.assertEqual("No hay usuarios nuevos para compartir la canción o los que están no pueden ser removidos.", response.json)

    def test_remover_usuarios_compartidos(self):
        """ Test que valida que no se intente remover un usuario compartido."""
        # Config
        headers = get_headers(self.app)
        payload = json.dumps({"usuarios_compartidos": ["Jacquette", "Cassi"]})
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)

        # Case 1
        payload = json.dumps({"usuarios_compartidos": ["Jacquette"]})
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(409, response.status_code)
        self.assertEqual("Los usuarios compartidos no pueden ser removidos.", response.json)

    def test_usuario_inexistente(self):
        """ Test que valida que el usuario al que se va a compartir exista"""
        # Config
        headers = get_headers(self.app)

        # Case 1
        payload = json.dumps({"usuarios_compartidos": ["Usuario-inexistente"]})
        endpoint = "cancion/1/usuarios-compartidos"
        response = self.app.post(endpoint, headers=headers, data=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual("El usuario: Usuario-inexistente, no existe.", response.json)



class TestModelosCompartirCancion(BaseCase):  # Siempre se debe heredar de base case
    """
    TestEjemploModelo ejecuta tests de modelo xxx
    """

    def test_crear_cancion(self):
        result = self.db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Nothing Else Matters")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "Metallica")
        self.assertEqual(result[0].usuario, 1)

    def test_compartir_cancion_con_duenio(self):
        excepcion_obtenida = None
        usuarios = self.db.session.query(Usuario)
        canciones = self.db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[0])
        try:
            canciones[0].usuarios_compartidos = usuarios_compartidos
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)

    def test_compartir_cancion_con_usuario(self):
        usuarios = self.db.session.query(Usuario)
        canciones = self.db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        canciones[0].usuarios_compartidos = usuarios_compartidos
        self.db.session.commit()

        result = self.db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Nothing Else Matters")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "Metallica")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_cancion_con_usuarios_y_duenio(self):
        usuarios = self.db.session.query(Usuario)
        canciones = self.db.session.query(Cancion)
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
        usuarios = self.db.session.query(Usuario)
        canciones = self.db.session.query(Cancion)
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
        self.db.session.commit()

        result = self.db.session.query(Cancion)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].titulo, "Nothing Else Matters")
        self.assertEqual(result[0].minutos, 4)
        self.assertEqual(result[0].segundos, 40)
        self.assertEqual(result[0].interprete, "Metallica")
        self.assertEqual(result[0].usuario, 1)
        self.assertEqual(result[0].usuarios_compartidos, usuarios_compartidos)

    def test_compartir_cancion_con_usuario_repetido(self):
        usuarios = self.db.session.query(Usuario)
        canciones = self.db.session.query(Cancion)
        usuarios_compartidos = []
        usuarios_compartidos.append(usuarios[1])
        usuarios_compartidos.append(usuarios[1])
        try:
            canciones[0].usuarios_compartidos = usuarios_compartidos
            self.db.session.commit()
        except Exception as e:
            excepcion_obtenida = e

        self.assertIsNotNone(excepcion_obtenida)
