import os
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

DATABASE_URL = os.environ['DATABASE_URL']

engine = sqlalchemy.create_engine(DATABASE_URL, convert_unicode=True)
session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = sqlalchemy.ext.declarative.declarative_base()
Base.query = session.query_property()

def init_db():
    import kantine.models
    Base.metadata.create_all(bind=engine)
