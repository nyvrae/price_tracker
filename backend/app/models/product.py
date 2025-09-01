from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    image_url = Column(String, nullable=False)
    prices = relationship(
        "Price",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    site = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    product = relationship("Product", back_populates="prices")