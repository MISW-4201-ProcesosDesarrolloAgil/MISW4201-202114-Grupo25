
# Flask
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Models
from flaskr.modelos.comentarios import ComentarioModel, ComentarioSchema
from flaskr.modelos.modelos import Album

# Utils
from flaskr.modelos.database import db
import logging

comentario_schema = ComentarioSchema()


class VistaComentarios(Resource):
    @jwt_required()
    def post(self, album_id):
        """
        Metodo post de la vista de comentarios.
        Añade un nuevo comentario a la base de datos

        :return: Comentario, Estatus Http 201
        """
        user_id = get_jwt_identity()

        descripcion = request.json.get('descripcion')
        if descripcion is None or descripcion =="":
            return {"message": "la descripcion no puede estar en blanco"}, 400

        album = Album.query.filter_by(id=album_id, usuario=user_id).first()
        if album is None:
            return {"message": "el album indicado no existe"}, 400

        comentario = ComentarioModel(
            descripcion=descripcion,
            album_id=album_id,
            user_id=user_id
        )

        try:
            db.session.add(comentario)
            db.session.commit()
        except Exception as e:
            logging.info(e)
            return {"error ": "internal error"}, 500

        return {
                   "message": "comentario creado satisfactoriamente",
                   "data": comentario_schema.dump(comentario),
               }, 201
