import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import datetime, timedelta, timezone

from app.models import Base, Product, Price
from app.crud.search import search_products


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_data(db_session):
    p1 = Product(title="Apple iPhone 13", url="url1", image_url="img1")
    p2 = Product(title="Samsung Galaxy S21", url="url2", image_url="img2")
    p3 = Product(title="Apple Watch Series 7", url="url3", image_url="img3")
    p4 = Product(title="Google Pixel 6", url="url4", image_url="img4")
    p5 = Product(title="Sony Headphones", url="url5", image_url="img5")
    db_session.add_all([p1, p2, p3, p4, p5])
    db_session.commit()

    now = datetime.now(timezone.utc)
    prices = [
        Price(product_id=p1.id, site="site1", price=Decimal("1000"), created_at=now),
        Price(product_id=p2.id, site="site1", price=Decimal("800"), created_at=now - timedelta(days=1)),
        Price(product_id=p3.id, site="site1", price=Decimal("500"), created_at=now),
        Price(product_id=p4.id, site="site1", price=Decimal("700"), created_at=now - timedelta(days=2)),
        Price(product_id=p5.id, site="site1", price=Decimal("200"), created_at=now),
        Price(product_id=p1.id, site="site2", price=Decimal("950"), created_at=now - timedelta(hours=1)),
        Price(product_id=p2.id, site="site2", price=Decimal("850"), created_at=now - timedelta(days=3)),
    ]
    db_session.add_all(prices)
    db_session.commit()

    return [p1, p2, p3, p4, p5]


def test_filter_by_title(db_session, sample_data):
    products = search_products(db_session, title="Apple")
    assert {p.title for p in products} == {"Apple iPhone 13", "Apple Watch Series 7"}

    products = search_products(db_session, title="Samsung")
    assert len(products) == 1 and products[0].title == "Samsung Galaxy S21"

    products = search_products(db_session, title="Pixel")
    assert len(products) == 1 and products[0].title == "Google Pixel 6"

    products = search_products(db_session, title="sony")
    assert len(products) == 1 and products[0].title == "Sony Headphones"

    products = search_products(db_session, title="NonExistent")
    assert products == []


def test_filter_by_min_max_price(db_session, sample_data):
    products = search_products(db_session, min_price=Decimal("900"))
    assert {p.title for p in products} == {"Apple iPhone 13"}

    products = search_products(db_session, max_price=Decimal("900"))
    assert {p.title for p in products} == {
        "Samsung Galaxy S21", "Apple Watch Series 7", "Google Pixel 6", "Sony Headphones"
    }

    products = search_products(db_session, min_price=Decimal("700"), max_price=Decimal("900"))
    assert {p.title for p in products} == {"Samsung Galaxy S21", "Google Pixel 6"}

    products = search_products(db_session, min_price=Decimal("800"), max_price=Decimal("800"))
    assert {p.title for p in products} == {"Samsung Galaxy S21"}

    products = search_products(db_session, min_price=Decimal("2000"))
    assert products == []

    products = search_products(db_session, max_price=Decimal("100"))
    assert products == []


def test_sorting(db_session, sample_data):
    products_asc = search_products(db_session, sort_by_price="asc")
    assert [p.title for p in products_asc] == [
        "Sony Headphones", "Apple Watch Series 7", "Google Pixel 6",
        "Samsung Galaxy S21", "Apple iPhone 13"
    ]

    products_desc = search_products(db_session, sort_by_price="desc")
    assert [p.title for p in products_desc] == [
        "Apple iPhone 13", "Samsung Galaxy S21", "Google Pixel 6",
        "Apple Watch Series 7", "Sony Headphones"
    ]

    products_title_asc = search_products(db_session, sort_by_price="asc", title="Apple")
    assert [p.title for p in products_title_asc] == [
        "Apple Watch Series 7", "Apple iPhone 13"
    ]


def test_no_filters(db_session, sample_data):
    products = search_products(db_session)
    assert len(products) == 5
    assert all(isinstance(p, Product) for p in products)


def test_edge_cases(db_session, sample_data):
    products = search_products(db_session, min_price=Decimal("0"), max_price=Decimal("10000"))
    assert len(products) == 5

    products = search_products(db_session, title="")
    assert len(products) == 5
