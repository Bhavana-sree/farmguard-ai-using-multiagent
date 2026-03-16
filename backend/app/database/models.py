from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.db import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    village = Column(String, nullable=False)
    language = Column(String, nullable=False)

    lands = relationship("Land", back_populates="farmer")


class Land(Base):
    __tablename__ = "lands"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    land_name = Column(String, nullable=True)

    farmer = relationship("Farmer", back_populates="lands")
    analyses = relationship("Analysis", back_populates="land")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    land_id = Column(Integer, ForeignKey("lands.id"), nullable=False)

    ndvi = Column(Float, nullable=True)
    estimated_trees = Column(Integer, nullable=True)
    carbon_credits = Column(Float, nullable=True)
    co2_kg = Column(Float, nullable=True)

    validation_status = Column(String, nullable=True)
    validation_reason = Column(Text, nullable=True)

    block_hash = Column(String, nullable=True)
    market_value_usd = Column(Float, nullable=True)

    land = relationship("Land", back_populates="analyses")
    purchases = relationship("Purchase", back_populates="analysis")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    industry = Column(String, nullable=False)

    purchases = relationship("Purchase", back_populates="company")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)

    credits_bought = Column(Float, nullable=False)
    price_per_credit_usd = Column(Float, nullable=False)
    total_price_usd = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="Completed")

    company = relationship("Company", back_populates="purchases")
    analysis = relationship("Analysis", back_populates="purchases")