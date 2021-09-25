from flask import request
from flaskr.modelos.modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from collections import OrderedDict
import sys
import logging

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
ERROR_REMOVER_USUARIOS = 'Los usuarios compartidos no pueden ser removidos.'


class VistaCanciones(Resource):

    def post(self):
        nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
        usuario = Usuario.query.get_or_404(request.json["id_usuario"])
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'La canción ya se compartió con el usuario ',409

        return cancion_schema.dump(nueva_cancion)

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        c_propias = Cancion.query.filter_by(usuario=user_id).all()
        c_propias_serializadas = [cancion_schema.dump(ca) for ca in c_propias]

        c_compartidas = Cancion.query.filter(Cancion.usuarios_compartidos.any(id=user_id)).all()
        c_compartidas_serializadas = [cancion_schema.dump(ca) for ca in c_compartidas]

        if len(c_compartidas + c_propias) == 0:
            return 'El usuario no tiene canciones compartidas ni propias.',400

        return (c_propias_serializadas + c_compartidas_serializadas), 200


class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))

    def put(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get("titulo",cancion.titulo)
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return '',204

class VistaAlbumesCanciones(Resource):
    def get(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        return [album_schema.dump(al) for al in cancion.albumes]

class VistaSignIn(Resource):
    
    def post(self):
        usuario = Usuario.query.filter_by(nombre =request.json["nombre"]).first()
        if usuario is not None:
            return 'El usuario ' + str(usuario.nombre) + ' ya existe en el sistema.',409
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}

class VistaAlbumsUsuario(Resource):
    """
    VistaAlbumUsuario se encarga de administrar los recursos relacionados a los albumes para un usuario dado
    """

    @jwt_required()
    def post(self):
        """
        Metodo post de la vista de comentarios.
        Añade un nuevo comentario a la base de datos

        :return: Album creado, Estatus Http 201
        """
        user_id = get_jwt_identity()
        nuevo_album = Album(
            titulo=request.json.get("titulo"),
            anio=request.json.get("anio"),
            descripcion=request.json.get("descripcion"),
            medio=request.json.get("medio"),
            usuario=user_id,
        )

        try:
            Album.crear_nuevo_album(nuevo_album)
        except Exception as e:
            return f"No se puede añadir album. Error: {e}", 400

        return album_schema.dump(nuevo_album), 201

    @jwt_required()
    def get(self):
        """
        Metodo get de la vista de comentarios.
        Añade un nuevo comentario a la base de datos

        :return: Album creado, Estatus Http 201
        """
        user_id = get_jwt_identity()

        a_propios = Album.query.filter_by(usuario=user_id).all()
        a_propias_serializadas = [album_schema.dump(al) for al in a_propios]

        a_compartidos = Album.query.filter(Album.usuarios_compartidos.any(id=user_id)).all()
        a_compartidas_serializadas = [album_schema.dump(al) for al in a_compartidos]

        if len(a_propias_serializadas + a_compartidas_serializadas) == 0:
            return 'El usuario no tiene albumes compartidos ni propios.', 400

        return (a_propias_serializadas + a_compartidas_serializadas), 200

class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))

    def put(self, id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get("titulo",album.titulo)
        album.anio = request.json.get("anio", album.anio)
        album.descripcion = request.json.get("descripcion", album.descripcion)
        album.medio = request.json.get("medio", album.medio)
        db.session.commit()
        return album_schema.dump(album)

    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return '',204

class VistaCancionesUsuariosCompartidos(Resource):

    @jwt_required()
    def post(self, id_cancion):
        """
            Método post de la vista de usuarios compartidos a una canción.
            Comparte una canción a un listado de usuarios
            :return: string, status code 200
        """

        result = self.validaciones_de_datos_de_cancion(id_cancion)
        if result != None:
            return result

        cancion = Cancion.query.get(id_cancion)
        [usuario_schema.dump(al) for al in cancion.usuarios_compartidos]

        nuevos_usuarios_compartidos = list(OrderedDict.fromkeys(request.json["usuarios_compartidos"]))
        result = validaciones_de_usuarios_compartidos('la canción', nuevos_usuarios_compartidos, cancion.usuarios_compartidos)
        if result != None:
            return result

        for i in range(len(cancion.usuarios_compartidos), len(nuevos_usuarios_compartidos)):
            new_user = Usuario.query.filter_by(nombre = nuevos_usuarios_compartidos[i]).first()
            if new_user is None:
                return "El usuario: " + nuevos_usuarios_compartidos[i] + ", no existe.", 404
            
            try:
                cancion.usuarios_compartidos.append(new_user)
            except ValueError:
                return 'La canción no puede ser compartida con el dueño de la misma.',409
        try:
            db.session.commit()
        except Exception as e:
            logging.info(e)
            return {"error ": "internal error"}, 500

        return 'Canción compartida.'

    def validaciones_de_datos_de_cancion(self, id_cancion):
        if id_cancion > sys.maxsize:
            return 'El campo id_cancion solo permite int como valor.',400

        cancion = Cancion.query.get(id_cancion)
        if cancion is None:
            return "La canción no existe", 404
        current_user = Usuario.query.get_or_404(get_jwt_identity())

        if cancion.usuario != current_user.id:
            return 'Solo el dueño de la canción puede compartirla.',400
        
        if isinstance(request.json["usuarios_compartidos"], list) == False:
            return 'El campo usuarios_compartidos solo permite array como valor.',400

    @jwt_required()
    def get(self, id_cancion):
        """
            Método get de la vista de usuarios compartidos a una canción.
            muestra el listado de usuarios que tienen compartida una canción
            :return: array[], status code 200
        """
        if id_cancion > sys.maxsize:
            return 'El campo id_cancion solo permite int como valor.',400

        cancion = Cancion.query.get(id_cancion)
        if cancion is None:
            return "La canción no existe.", 404
    
        [usuario_schema.dump(al) for al in cancion.usuarios_compartidos]

        current_user = Usuario.query.get_or_404(get_jwt_identity())
        if cancion.usuario != current_user.id:
            return 'Solo el dueño de la canción puede ver con quién la compartió.',400

        usuarios_compartidos = []
        for i in range(len(cancion.usuarios_compartidos)):
            usuarios_compartidos.append(cancion.usuarios_compartidos[i].nombre)

        return {"usuarios_compartidos": usuarios_compartidos}

class VistaAlbumesUsuariosCompartidos(Resource):
    
    @jwt_required()
    def post(self, id_album):
        """
            Método post de la vista de usuarios compartidos a un álbum.
            Comparte un álbum a un listado de usuarios
            :return: string, status code 200
        """
        result = self.validaciones_de_datos_de_album(id_album)
        if result != None:
            return result

        album = Album.query.get(id_album)
        [usuario_schema.dump(al) for al in album.usuarios_compartidos]

        nuevos_usuarios_compartidos = list(OrderedDict.fromkeys(request.json["usuarios_compartidos"]))
        result = validaciones_de_usuarios_compartidos('el álbum', nuevos_usuarios_compartidos, album.usuarios_compartidos)
        if result != None:
            return result

        for i in range(len(album.usuarios_compartidos), len(nuevos_usuarios_compartidos)):
            new_user = Usuario.query.filter_by(nombre = nuevos_usuarios_compartidos[i]).first()
            if new_user is None:
                return "El usuario: " + nuevos_usuarios_compartidos[i] + ", no existe.", 404
            
            try:
                album.usuarios_compartidos.append(new_user)
            except ValueError:
                return 'El álbum no puede ser compartido con el dueño del mismo.',409
        try:
            db.session.commit()
        except Exception as e:
            logging.info(e)
            return {"error ": "internal error"}, 500

        return 'Álbum compartido.'

    def validaciones_de_datos_de_album(self, id_album):
        if id_album > sys.maxsize:
            return 'El campo id_album solo permite int como valor.',400

        album = Album.query.get(id_album)
        if album is None:
            return "El álbum no existe", 404
        current_user = Usuario.query.get_or_404(get_jwt_identity())

        if album.usuario != current_user.id:
            return 'Solo el dueño del álbum puede compartirlo.',400

        if isinstance(request.json["usuarios_compartidos"], list) == False:
            return 'El campo usuarios_compartidos solo permite array como valor.',400

    @jwt_required()
    def get(self, id_album):
        """
            Método get de la vista de usuarios compartidos a un álbum.
            muestra el listado de usuarios que tienen compartido un álbum
            :return: array[], status code 200
        """
        if id_album > sys.maxsize:
            return 'El campo id_album solo permite int como valor.',400

        album = Album.query.get(id_album)
        if album is None:
            return "El álbum no existe.", 404
    
        [usuario_schema.dump(al) for al in album.usuarios_compartidos]

        current_user = Usuario.query.get_or_404(get_jwt_identity())
        if album.usuario != current_user.id:
            return 'Solo el dueño del álbum puede ver con quién lo compartió.',400

        usuarios_compartidos = []
        for i in range(len(album.usuarios_compartidos)):
            usuarios_compartidos.append(album.usuarios_compartidos[i].nombre)

        return {"usuarios_compartidos": usuarios_compartidos}

def validaciones_de_usuarios_compartidos(origen, nuevos_usuarios_compartidos, usuarios_compartidos):
        if len(nuevos_usuarios_compartidos) == 0:
            return 'No hay usuarios para compartir '+origen+'.',400

        if len(nuevos_usuarios_compartidos) == len(usuarios_compartidos):
            return 'No hay usuarios nuevos para compartir '+origen+' o los que están no pueden ser removidos.',400
        
        if len(nuevos_usuarios_compartidos) < len(usuarios_compartidos):
            return ERROR_REMOVER_USUARIOS,409 

        for i in range(len(usuarios_compartidos)): 
            if usuarios_compartidos[i].nombre != nuevos_usuarios_compartidos[i]:
                return ERROR_REMOVER_USUARIOS,409 