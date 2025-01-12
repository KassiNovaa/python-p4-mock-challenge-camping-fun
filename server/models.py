from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    # Add serialization rules

    serialize_rules = ( '-signups.activity', )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship

    signups = db.relationship( 'Signup' , back_populates = 'activity', cascade = 'all, delete-orphan' )
    campers = association_proxy( 'signups' , 'camper' )

    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    # Add serialization rules

    serialize_rules  = ('-signups.camper',)


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signups = db.relationship( 'Signup' , back_populates = 'camper' )
    
    # association_proxy allows you to easily connect the remainder relationships. the first arg is "what you have many of" the second arg is what you want to pull out of the first arg or instance
    activities = association_proxy( 'signups', 'activity' )

    
    # Add validation

    @validates ('name')
    def validates_name( self, key, new_name ):
        if new_name:
            return new_name
        raise ValueError('must have name')
    
    @validates ('age')
    def validates_age( self, key, new_age ):
        if 8 <= new_age <= 18:
            return new_age
        raise ValueError( 'age must be between 8 & 18' )
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    # Add serialization rules
    serialize_rules = ( '-camper.signups', '-activity.signups', )
 
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    # first add these columns to the has many method
    camper_id = db.Column( db.Integer, db.ForeignKey('campers.id') )
    activity_id = db.Column( db.Integer, db.ForeignKey('activities.id') )

    # Add relationships
    # then add the relationships from the methods you want to connect. back_populates is the variable you will create in the other methods that will join the tables together. 

    camper = db.relationship( 'Camper', back_populates = 'signups' )
    activity = db.relationship( 'Activity', back_populates = 'signups' )
    
    # Add validation
    @validates ('time')
    def validates_time( self, key, new_time ):
        if 0<= new_time <= 23:
            return new_time
        raise ValueError( 'time must be between 0 and 23' )
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
