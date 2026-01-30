from ..session import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

class RevokedToken(Base):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True, nullable=False)  # JWT ID
    token = Column(String, nullable=False)
    revoked_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
