from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class RunModel(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
