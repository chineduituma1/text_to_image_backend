import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative


DATABASE_URL = "sqlite:///./database.db"

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()