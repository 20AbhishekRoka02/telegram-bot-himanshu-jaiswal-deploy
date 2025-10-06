from sqlmodel import create_engine

from dotenv import load_dotenv
import os
load_dotenv()

# DATABASE_URL=f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@{os.environ['CONTAINER_NAME']}:{os.environ['DB_PORT']}/{os.environ['MYSQL_DATABASE']}"
DATABASE_URL=os.environ['DATABASE_URL']


# sqlite_file_name = "schoolerp.db"
# sqlite_url = f"sqlite:///./{sqlite_file_name}"

engine = create_engine(DATABASE_URL, 
  echo=True,
  pool_pre_ping=True,   # Auto-checks if connection is alive
  pool_recycle=1800,    # Reconnect every 30 min to avoid timeout
  pool_size=5,          # Controls how many connections are kept open
  max_overflow=10      # Allows temporary extra connections
  )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
