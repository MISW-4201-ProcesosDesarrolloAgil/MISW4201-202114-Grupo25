# Modelo Comentarios

# SqlAlchemy
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flaskr.modelos.database import db

# Utils
import datetime


class ComentarioModel(db.Model):
    """
    Comentario representa el modelo de un comentario de una publicacion.
    """
    __tablename__ = 'comentarios'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(length=1000), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # ToDo: Incluir relaciones

class ComentarioSchema(SQLAlchemyAutoSchema):
    """
    ComentarioSchema serializa la informacion del modelo comentario.
    """
    class Meta:
        model = ComentarioModel
        # ToDo: Incluir relaciones