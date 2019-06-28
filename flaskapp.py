# EXTERNAL PACKAGES
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, inspect
from sqlalchemy.ext.hybrid import hybrid_property
from flask_migrate import Migrate
import pandas as pd
# PYTHON STANDARD LIBRARY
import os
import csv

# CONFIGURE APPLICATION
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class BaseMixin(object):
    """Methods and properties inherited by all models"""
    # COLUMNS
    id = db.Column(db.Integer, primary_key=True)
    
    @hybrid_property
    def columns(self):
        """Return columns of model"""
        return self.__table__.columns.keys()

    @classmethod
    def dataframe(cls):
        """Return pandas dataframe of table data"""
        data = [{k: v for (k, v) in vars(obj).items() if k in obj.columns} for obj in cls.query.all()]
        return pd.DataFrame.from_records(data)

    @classmethod
    def create(cls, **kw):
        """Create class object and save to database"""
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def get(cls, id):
        """Return one object where id=id"""
        return db.session.query(cls).filter_by(id=id).one_or_none()

    @classmethod
    def unique(cls, **kw):
        """Return one object where kw=value and kw is a column with unique constraint"""
        return db.session.query(cls).filter_by(**kw).one_or_none()

    @classmethod
    def all(cls):
        """Return all objects of class"""
        return db.session.query(cls).all()

    @classmethod
    def filter_by(cls, **kw):
        """Return objects using filter of kwarg=value"""
        return db.session.query(cls).filter_by(**kw)


class MyModel(db.Model, BaseMixin):
    __tablename__ = 'my_model'
    
    # COLUMNS
    column1 = db.Column(db.String, unique=True, nullable=False)
    column2 = db.Column(db.Integer)
    column3 = db.Column(db.Decimal)
    
    
@app.route('/')
def index():
    df = FirstModel.dataframe()
    return(df.to_html)
    
if __name__ == '__main__':
    app.run(debug=True)
