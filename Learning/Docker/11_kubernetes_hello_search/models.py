from sqlmodel import SQLModel, Field, create_engine, Session
from dotenv import load_dotenv
import os


# Load environment variables from a .env file
load_dotenv()


# Get the database URL from environment variables
db_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(f"{db_url}", echo=True)


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)


def create_tables():
    print("\nCreating database tables...\n")
    SQLModel.metadata.create_all(engine)
    print("\nTables created successfully.\n")


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    create_tables()