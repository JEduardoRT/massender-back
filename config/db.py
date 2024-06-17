from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:15022000@localhost:3306/prueba_fastapi")
#engine = create_engine("mysql+pymysql://root:QNnWLOhCHwZyHOuPbpzsDKnOwEsolCdF@roundhouse.proxy.rlwy.net:56585/railway")
#engine = create_engine("mysql://root:QNnWLOhCHwZyHOuPbpzsDKnOwEsolCdF@mysql.railway.internal:3306/railway")

meta = MetaData()

conn = engine.connect()
