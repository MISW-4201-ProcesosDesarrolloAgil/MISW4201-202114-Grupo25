from flaskr import create_app
from flask_restful import Api
from .modelos import db
from .vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum, \
    VistaLogIn, VistaAlbumesCanciones
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from flask import Flask
from flask_restplus import Resource, Api

application = Flask(__name__)
api = Api(application,
          version='0.1',
          title='Our sample API',
          description='This is our sample API',
          )


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


if __name__ == '__main__':
    application.run(debug=True)

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')

jwt = JWTManager(app)
