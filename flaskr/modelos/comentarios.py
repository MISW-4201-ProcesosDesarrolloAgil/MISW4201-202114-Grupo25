# Modelo Comentarios

# SqlAlchemy
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flaskr.modelos.database import db
from sqlalchemy.orm import validates


# Utils
import datetime


class ComentarioModel(db.Model):
    """
    Comentario representa el modelo de un comentario de una publicacion.
    """
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(length=1000), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    # ToDo: Incluir relaciones

    @validates('descripcion')
    def validar_descripcion(self, key, value):
        """ validar_descripcion se asegura que la descripcion no este vacia"""
        if len(value) == 0:
            raise ValueError
        return value


class ComentarioSchema(SQLAlchemyAutoSchema):
    """
    ComentarioSchema serializa la informacion del modelo comentario.
    """
    class Meta:
        model = ComentarioModel
        include_relationships = False