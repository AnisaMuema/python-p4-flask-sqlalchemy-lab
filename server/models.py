from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Zookeeper(db.Model, SerializerMixin):
    __tablename__ = 'zookeepers'
    serialize_rules = ('-animals.zookeeper',)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birthday = db.Column(db.String)

    animals = db.relationship('Animal', backref='zookeeper')

class Enclosure(db.Model, SerializerMixin):
    __tablename__ = 'enclosures'
    serialize_rules = ('-animals.enclosure',)
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String)
    open_to_visitors = db.Column(db.Boolean)

    animals = db.relationship('Animal', backref='enclosure')

    def __repr__(self):
        return f'Enclosure {self.environment}'

class Animal(db.Model, SerializerMixin):
    __tablename__ = 'animals'
    serialize_rules = ('-enclosure.animals', '-zookeeper.animals')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeepers.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosures.id'))

    def __repr__(self):
        return f'Animal {self.name}'
