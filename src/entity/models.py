from datetime import date, datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import Date, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    description: Mapped[str] = mapped_column(String(250), nullable=True, default=None)
    date_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    last_visit: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    @hybrid_property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"
