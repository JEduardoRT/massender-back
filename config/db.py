from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:15022000@localhost:3306/prueba_fastapi"
#DATABASE_URL = "mysql+pymysql://root:QNnWLOhCHwZyHOuPbpzsDKnOwEsolCdF@roundhouse.proxy.rlwy.net:56585/railway"
DATABASE_URL = "mysql://root:QNnWLOhCHwZyHOuPbpzsDKnOwEsolCdF@mysql.railway.internal:3306/railway"
"""

username = 'JandryRT15'
password = 'Aiu18QlS7vw'
host = 'JandryRT15.mysql.pythonanywhere-services.com'
database = 'JandryRT15$default'

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/{database}"

"""

engine = create_engine(DATABASE_URL)
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
conn = engine.connect()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
