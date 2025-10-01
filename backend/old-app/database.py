from sqlmodel import create_engine

from dotenv import load_dotenv
import os
load_dotenv()

# DATABASE_URL=f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}@placement_portal_db:3306/{os.environ['MYSQL_DATABASE']}"


# sqlite_file_name = "schoolerp.db"
# sqlite_url = f"sqlite:///./{sqlite_file_name}"

# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)