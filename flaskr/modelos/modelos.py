from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow import fields
import enum
from sqlalchemy.orm import validates

# Database
from flaskr.modelos.database import db

albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

usuarios_canciones_compartidas = db.Table('usuario_cancion_compartida',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

usuarios_albumes_compartidos = db.Table('usuario_album_compartido',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True))

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates="canciones")
    usuarios_compartidos = db.relationship('Usuario', secondary = 'usuario_cancion_compartida', back_populates="canciones_compartidas")

    @validates('usuarios_compartidos')
    def validate_usuarios_compartidos(self, key, value):
        if value.id == self.usuario:
            raise ValueError
        return value

class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3

class Album(db.Model):
    __tablname__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates="albumes")
    usuarios_compartidos = db.relationship('Usuario', secondary = 'usuario_album_compartido', back_populates="albumes_compartidos")

    @validates('usuarios_compartidos')
    def validate_usuarios_compartidos(self, key, value):
        if value.id == self.usuario:
            raise ValueError
        return value

    @classmethod
    def crear_nuevo_album(self, album):
        """
        Añade un nuevo album a los albumes del usuario
        """
        db.session.add(album)
        db.session.commit()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')
    canciones = db.relationship('Cancion', cascade='all, delete, delete-orphan')
    canciones_compartidas = db.relationship('Cancion', secondary = 'usuario_cancion_compartida', back_populates="usuarios_compartidos")
    albumes_compartidos = db.relationship('Album', secondary = 'usuario_album_compartido', back_populates="usuarios_compartidos")


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Cancion
         include_relationships = True
         load_instance = True
         include_fk = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("medio"))
    class Meta:
         model = Album
         include_relationships = True
         load_instance = True
         include_fk = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class UsuarioBaseSchema(SQLAlchemySchema):
    """
    Schema con la informacion base de un usuario
    """
    class Meta:
        model = Usuario
    id = auto_field()
    nombre = auto_field()
