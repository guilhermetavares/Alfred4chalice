from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite://")
Base = declarative_base()
Session = orm.scoped_session(orm.sessionmaker(bind=engine))
