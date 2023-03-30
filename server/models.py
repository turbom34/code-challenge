from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    serialize_rules = ('-vendors.sweets', '-vendor_sweets.sweets')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref='sweet')

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    serialize_rules = ('-vendor_sweets.sweet', '-vendor_sweets.vendor')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    vendor_sweets = db.relationship('VendorSweet', backref='vendor')

class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    serialize_rules = ('-vendor.vendor_sweets', '-sweet.vendor_sweets')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    sweets_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))


    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError('Price cannot be negative')
        return price

# for relationships between tables, name these "vendor_sweets"