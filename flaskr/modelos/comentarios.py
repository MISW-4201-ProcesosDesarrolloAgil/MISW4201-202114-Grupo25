# Modelo Comentarios

# SqlAlchemy
from marshmallow_sqlalchemy import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import validates

# Models
from flaskr.modelos.database import db
from flaskr.modelos.modelos import UsuarioBaseSchema

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

    user = db.relationship("Usuario", backref="comentario")

    @validates('descripcion')
    def validar_descripcion(self, key, value):
        """ validar_descripcion se asegura que la descripcion no este vacia"""
        if len(value) == 0:
            raise ValueError
        return value

    @classmethod
    def get_by_album(self, album_id):
        """ get_by_album devuelve los comentarios para un album determinado en orden descendente"""
        return self.query.filter_by(album_id=album_id).order_by(ComentarioModel.fecha_creacion.desc())

class ComentarioSchema(SQLAlchemyAutoSchema):
    """
    ComentarioSchema serializa la informacion del modelo comentario.
    """

    class Meta:
        model = ComentarioModel
        include_relationships = True
        load_instance = True
    user = fields.Nested(UsuarioBaseSchema)
