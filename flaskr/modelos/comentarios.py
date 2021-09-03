# Modelo Comentarios

# SqlAlchemy
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class ComentarioModel(db.Model):
    """
    Comentario representa el modelo de un comentario de una publicacion.
    """


class ComentarioSchema(SQLAlchemyAutoSchema):
    """
    ComentarioSchema serializa la informacion del modelo comentario.
    """
    pass