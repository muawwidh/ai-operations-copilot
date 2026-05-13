from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)

    processed_status = Column(String(50), nullable=False, default="Pending", index=True)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chunks = relationship("DocumentChunk", back_populates="document")