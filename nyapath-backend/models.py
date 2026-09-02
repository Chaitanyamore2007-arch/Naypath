import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from database import Base

# Utility to support both SQLite (which doesn't have native UUID/JSONB) and Postgres
# For the prototype, we'll use generic types that fallback gracefully.
from sqlalchemy.types import TypeDecorator, CHAR

class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    profile_hash = Column(String, unique=True, index=True)
    industry_type = Column(String)
    district = Column(String)
    investment_scale_crores = Column(Numeric)
    roadmap_json = Column(JSON) # JSONB in postgres
    created_at = Column(DateTime, default=datetime.utcnow)

    audits = relationship("Audit", back_populates="roadmap")


class Clearance(Base):
    __tablename__ = "clearances"

    id = Column(String, primary_key=True)
    name = Column(String)
    department = Column(String)
    applicable_industries = Column(JSON) # Array in Postgres
    required_documents = Column(JSON)
    estimated_days_min = Column(Integer)
    estimated_days_max = Column(Integer)
    estimated_fee_inr = Column(Numeric)
    typical_rejection_reasons = Column(JSON)


class Audit(Base):
    __tablename__ = "audits"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(GUID, ForeignKey("roadmaps.id"))
    gaps_json = Column(JSON)
    compliant_count = Column(Integer)
    gap_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    roadmap = relationship("Roadmap", back_populates="audits")
