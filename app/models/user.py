from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_or_email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    hashed_pin = Column(String, nullable=True) # PIN secondaire
    pseudo = Column(String, nullable=True) # Faux nom
    
    # Rôles: user, psychologist, lawyer, ngo, admin
    role = Column(String, default="user")
    
    # Panic Mode
    panic_mode_active = Column(Boolean, default=False)
    panic_mode_activated_at = Column(DateTime(timezone=True), nullable=True)
    local_wipe_requested = Column(Boolean, default=False)
    server_data_retained = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
