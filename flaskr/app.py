# Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Modelos
from flaskr.modelos.database import db

# Vistas
from flaskr.vistas.comentario import VistaComentarios
from flaskr.vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, \
    VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaCancionesUsuariosCompartidos, \
    VistaAlbumesUsuariosCompartidos

# Utils
from . import create_app

app = create_app()

app_context = app.app_context()
app_context.push()

# Declare API
api = Api(app)
cors = CORS(app)
jwt = JWTManager(app)

# Initialize Database
db.init_app(app)
db.create_all()

# Initialize Routes
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumsUsuario, '/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaCancionesUsuariosCompartidos, '/cancion/<int:id_cancion>/usuarios-compartidos')
api.add_resource(VistaComentarios, '/album/<int:album_id>/comentario')
api.add_resource(VistaAlbumesUsuariosCompartidos, '/album/<int:id_album>/usuarios-compartidos')
