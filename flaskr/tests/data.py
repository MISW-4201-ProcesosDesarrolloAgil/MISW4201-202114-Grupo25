# Modelos

from flaskr.modelos.modelos import Usuario, Cancion, Album

def seed_data(db):
    """seed_data se encarga de añadir datos de prueba con fines de testing"""
    db.session.add(Usuario(id=1, nombre="Enrique", contrasena="H0zksFgA8k6"))
    db.session.add(Usuario(id=2, nombre="Jacquette", contrasena="CMN3W3HoZe"))
    db.session.add(Usuario(id=3, nombre="Cassi", contrasena="FAjq5MZ"))
    db.session.add(Usuario(id=4, nombre="Lauren", contrasena="Czk0OhCOLKTk"))
    db.session.add(Usuario(id=5, nombre="Wylie", contrasena="MnCuMbNyB"))
    db.session.add(Usuario(id=6, nombre="Madalyn", contrasena="Z2JD1Jxi"))
    db.session.add(Usuario(id=7, nombre="Damaris", contrasena="VXxxKza4"))
    db.session.add(Usuario(id=8, nombre="Jannel", contrasena="gtN4DhfSMgY"))
    db.session.add(Usuario(id=9, nombre="Myca", contrasena="bIbrbO0P"))
    db.session.add(Usuario(id=10,nombre="Gene", contrasena="nTXjUeTV"))

    db.session.add(Album(id=1, titulo='Urban Menace', anio=1987, descripcion='monetize mission-critical ROI', usuario=1))
    db.session.add(Album(id=2, titulo='Loft', anio=2008, descripcion='engineer scalable bandwidth', usuario=2))
    db.session.add(Album(id=3, titulo='Warped Ones, The (Kyonetsu no kisetsu)', anio=2007, descripcion='evolve global deliverables', usuario=3))
    db.session.add(Album(id=4, titulo='Aral, Fishing in an Invisible Sea', anio=1999, descripcion='grow virtual communities', usuario=4))
    db.session.add(Album(id=5, titulo='Entracte', anio=1990, descripcion='transition e-business niches', usuario=5))
    db.session.add(Album(id=6, titulo='Commando', anio=2010, descripcion='brand magnetic content', usuario=6))
    db.session.add(Album(id=7, titulo='101 Dalmatians II: Patch''s London Adventure', anio=2006, descripcion='extend enterprise e-tailers', usuario=7))
    db.session.add(Album(id=8, titulo='Time for Killing, A', anio=1996, descripcion='enhance seamless portals', usuario=8))
    db.session.add(Album(id=9, titulo='Hardcore', anio=1987, descripcion='grow scalable e-markets', usuario=9))
    db.session.add(Album(id=10, titulo='Appaloosa', anio=1986, descripcion='unleash turn-key e-services', usuario=10))
    db.session.add(Album(id=11, titulo='Final Destination 5', anio=1994, descripcion='morph virtual ROI', usuario=1))
    db.session.add(Album(id=12, titulo='Outbreak', anio=2000, descripcion='integrate e-business technologies', usuario=2))
    db.session.add(Album(id=13, titulo='Three Musketeers, The', anio=2010, descripcion='innovate interactive portals', usuario=1))
    db.session.add(Album(id=14, titulo='Presumed Guilty (Presunto culpable)', anio=2003,descripcion='visualize wireless experiences', usuario=2))
    db.session.add(Album(id=15, titulo='I Am Curious (Yellow) (Jag är nyfiken - en film i gult)', anio=2007, descripcion='synergize user-centric partnerships', usuario=5))
    db.session.add(Album(id=16, titulo='Rage (Rabia)', anio=2002, descripcion='whiteboard intuitive bandwidth', usuario=6))
    db.session.add(Album(id=17, titulo='Heaven''s Gate', anio=1995, descripcion='expedite transparent methodologies', usuario=3))
    db.session.add(Album(id=18, titulo='Low Down Dirty Shame, A', anio=2007, descripcion='synthesize sticky metrics', usuario=18))
    db.session.add(Album(id=19, titulo='Saw V', anio=1991, descripcion='visualize magnetic communities', usuario=5))
    db.session.add(Album(id=20, titulo='Kevin Smith: Sold Out - A Threevening with Kevin Smith', anio=1993, descripcion='exploit B2C channels', usuario=7))
    db.session.add(Cancion(titulo="titulo", minutos=4, segundos=40, interprete="interprete", usuario=1))
    db.session.commit()

