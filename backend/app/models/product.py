from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    user_products = relationship("UserProducts", back_populates="user", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    prices = relationship(
        "Price",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_products = relationship("UserProducts", back_populates="product", cascade="all, delete-orphan")

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    site = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    product = relationship("Product", back_populates="prices")

class UserProducts(Base):
    __tablename__ = "user_products"
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='user_product_uc'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    favorite = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="user_products")
    product = relationship("Product", back_populates="user_products")
