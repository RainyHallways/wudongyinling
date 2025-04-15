from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blood_pressure = Column(String(20))  # 格式: "120/80"
    heart_rate = Column(Integer)
    blood_sugar = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="health_records") 