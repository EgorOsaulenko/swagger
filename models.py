import os
from typing import Optional
from sqlalchemy import String, Text, create_engine
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, Session
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_URI = os.getenv("SQLALCHEMY_URI")
engine = create_engine(SQLALCHEMY_URI, echo=True)
Base = declarative_base()

class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    age: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    illness: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

# Base.metadata.create_all(bind=engine)

async def get_db():
    with Session(bind=engine) as session:
        yield session
