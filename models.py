"""Data models for tables in the database."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()


class ItunesSubscription(Base):
    """Entity for itunes subscription."""

    __tablename__ = "itunes_subscription"
    __table_args__ = {"schema": "public"}

    id = Column(String(64), primary_key=True)
    transactions = Column(JSONB)
    trial_start_date = Column(DateTime, nullable=True)
    subscription_start_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime)
    current_status = Column(String(64))
