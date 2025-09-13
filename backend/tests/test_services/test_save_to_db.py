import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.product import Base, Product, Price
from app.services import save_to_db
import logging

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)

@pytest.mark.parametrize(
    "price_str,expected",
    [
        ("$123.45", Decimal("123.45")),
        ("123,45", Decimal("123.45")),
        ("USD 99.99", Decimal("99.99")),
        ("N/A", Decimal("0.00")),
        ("abc", Decimal("0.00")),
        ("", Decimal("0.00")),
        ("$1,234.56", Decimal("1234.56")),
    ]
)
def test_parse_price(price_str, expected):
    assert save_to_db.parse_price(price_str) == expected

def test_save_products_new(db_session):
    products = [
        {"title": "Test Product 1", "url": "url1", "image_url": "img1", "price": "$100"},
        {"title": "Test Product 2", "url": "url2", "image_url": "img2", "price": "N/A"},
    ]
    save_to_db.save_products(db_session, products)

    db_products = db_session.query(Product).all()
    db_prices = db_session.query(Price).all()
    
    assert len(db_products) == 2
    assert len(db_prices) == 2
    assert db_prices[0].price == Decimal("100")
    assert db_prices[1].price is None

def test_save_products_existing_product(db_session):
    product = Product(title="Existing", url="url_existing", image_url="img")
    db_session.add(product)
    db_session.commit()

    products = [
        {"title": "Existing", "url": "url_existing", "image_url": "img", "price": "$50"}
    ]
    save_to_db.save_products(db_session, products)

    db_products = db_session.query(Product).filter_by(url="url_existing").all()
    db_prices = db_session.query(Price).filter_by(product_id=product.id).all()

    assert len(db_products) == 1
    assert len(db_prices) == 1
    assert db_prices[0].price == Decimal("50")

def test_save_products_invalid_price(db_session, caplog):
    products = [
        {"title": "Bad Price", "url": "url_bad", "image_url": "img", "price": "abc"}
    ]
    caplog.set_level(logging.WARNING)
    save_to_db.save_products(db_session, products)

    db_prices = db_session.query(Price).join(Product).filter(Product.url=="url_bad").all()
    assert len(db_prices) == 1
    assert db_prices[0].price == Decimal("0.00")
    assert any("Failed to parse price" in record.message for record in caplog.records)

def test_save_products_exception_handling_and_rollback(db_session, caplog):
    products = [
        {"title": "Valid Product", "url": "url_valid", "price": "100"},
        {"url": "invalid_product", "price": "200"}
    ]
    
    save_to_db.save_products(db_session, products)

    assert db_session.query(Product).count() == 1
    assert db_session.query(Price).count() == 1
    assert any("Error saving product" in record.message for record in caplog.records)