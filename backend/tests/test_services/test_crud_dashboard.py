import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import datetime, timedelta, timezone

from app.models import Base, Product, Price, User, UserProducts
from app.crud.search_dashboard import search_dashboard_products

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
    user1 = User(email="user1@test.com", password_hash="hash1")
    user2 = User(email="user2@test.com", password_hash="hash2")
    user3 = User(email="user3@test.com", password_hash="hash3")
    db_session.add_all([user1, user2, user3])
    db_session.commit()

    product1 = Product(title="Apple iPhone 13", url="url1", image_url="img1")
    product2 = Product(title="Samsung Galaxy S21", url="url2", image_url="img2")
    product3 = Product(title="Apple Watch Series 7", url="url3", image_url="img3")
    product4 = Product(title="Google Pixel 6", url="url4", image_url="img4")
    product5 = Product(title="Sony Headphones", url="url5", image_url="img5")
    db_session.add_all([product1, product2, product3, product4, product5])
    db_session.commit()

    now = datetime.now(timezone.utc)
    price1 = Price(product_id=product1.id, site="site1", price=Decimal("1000"), created_at=now)
    price2 = Price(product_id=product2.id, site="site1", price=Decimal("800"), created_at=now - timedelta(days=1))
    price3 = Price(product_id=product3.id, site="site1", price=Decimal("500"), created_at=now)
    price4 = Price(product_id=product4.id, site="site1", price=Decimal("700"), created_at=now - timedelta(days=2))
    price5 = Price(product_id=product5.id, site="site1", price=Decimal("200"), created_at=now)
    price6 = Price(product_id=product1.id, site="site2", price=Decimal("950"), created_at=now - timedelta(hours=1))
    price7 = Price(product_id=product2.id, site="site2", price=Decimal("850"), created_at=now - timedelta(days=3))
    db_session.add_all([price1, price2, price3, price4, price5, price6, price7])
    db_session.commit()

    up1 = UserProducts(user_id=user1.id, product_id=product1.id, favorite=True)
    up2 = UserProducts(user_id=user1.id, product_id=product2.id, favorite=False)
    up3 = UserProducts(user_id=user2.id, product_id=product3.id, favorite=True)
    up4 = UserProducts(user_id=user1.id, product_id=product4.id, favorite=True)
    up5 = UserProducts(user_id=user2.id, product_id=product5.id, favorite=False)
    up6 = UserProducts(user_id=user3.id, product_id=product1.id, favorite=False)
    up7 = UserProducts(user_id=user3.id, product_id=product5.id, favorite=True)
    db_session.add_all([up1, up2, up3, up4, up5, up6, up7])
    db_session.commit()

    return {"user1": user1, "user2": user2, "user3": user3, "products": [product1, product2, product3, product4, product5]}

def test_filter_by_user(db_session, sample_data):
    user1 = sample_data["user1"]
    products = search_dashboard_products(db_session, user_id=user1.id)
    assert len(products) == 3
    assert all(isinstance(p, Product) for p in products)
    assert {p.title for p in products} == {"Apple iPhone 13", "Samsung Galaxy S21", "Google Pixel 6"}

    user2 = sample_data["user2"]
    products = search_dashboard_products(db_session, user_id=user2.id)
    assert len(products) == 2
    assert {p.title for p in products} == {"Apple Watch Series 7", "Sony Headphones"}

    user3 = sample_data["user3"]
    products = search_dashboard_products(db_session, user_id=user3.id)
    assert len(products) == 2
    assert {p.title for p in products} == {"Apple iPhone 13", "Sony Headphones"}

    products = search_dashboard_products(db_session, user_id=999)
    assert len(products) == 0

def test_only_favorites(db_session, sample_data):
    user1 = sample_data["user1"]
    products = search_dashboard_products(db_session, user_id=user1.id, only_favorites=True)
    assert len(products) == 2
    assert {p.title for p in products} == {"Apple iPhone 13", "Google Pixel 6"}

    user2 = sample_data["user2"]
    products = search_dashboard_products(db_session, user_id=user2.id, only_favorites=True)
    assert len(products) == 1
    assert products[0].title == "Apple Watch Series 7"

    user3 = sample_data["user3"]
    products = search_dashboard_products(db_session, user_id=user3.id, only_favorites=True)
    assert len(products) == 1
    assert products[0].title == "Sony Headphones"

    products = search_dashboard_products(db_session, user_id=999, only_favorites=True)
    assert len(products) == 0

def test_filter_by_title(db_session, sample_data):
    user1 = sample_data["user1"]
    products = search_dashboard_products(db_session, user_id=user1.id, title="Apple")
    assert len(products) == 1
    assert products[0].title == "Apple iPhone 13"

    products = search_dashboard_products(db_session, user_id=user1.id, title="Samsung")
    assert len(products) == 1
    assert products[0].title == "Samsung Galaxy S21"

    products = search_dashboard_products(db_session, user_id=user1.id, title="Pixel")
    assert len(products) == 1
    assert products[0].title == "Google Pixel 6"

    products = search_dashboard_products(db_session, user_id=user1.id, title="apple")
    assert len(products) == 1
    assert products[0].title == "Apple iPhone 13"

    products = search_dashboard_products(db_session, user_id=user1.id, title="iPh")
    assert len(products) == 1
    assert products[0].title == "Apple iPhone 13"

    products = search_dashboard_products(db_session, user_id=user1.id, title="NonExistent")
    assert len(products) == 0

def test_filter_by_min_max_price(db_session, sample_data):
    user1 = sample_data["user1"]
    products = search_dashboard_products(db_session, user_id=user1.id, min_price=Decimal("900"))
    assert len(products) == 1
    assert products[0].title == "Apple iPhone 13"

    products = search_dashboard_products(db_session, user_id=user1.id, max_price=Decimal("900"))
    assert len(products) == 2
    assert {p.title for p in products} == {"Samsung Galaxy S21", "Google Pixel 6"}

    products = search_dashboard_products(db_session, user_id=user1.id, min_price=Decimal("700"), max_price=Decimal("900"))
    assert len(products) == 2
    assert {p.title for p in products} == {"Samsung Galaxy S21", "Google Pixel 6"}

    products = search_dashboard_products(db_session, user_id=user1.id, min_price=Decimal("800"), max_price=Decimal("800"))
    assert len(products) == 1
    assert products[0].title == "Samsung Galaxy S21"

    products = search_dashboard_products(db_session, user_id=user1.id, min_price=Decimal("2000"))
    assert len(products) == 0

    products = search_dashboard_products(db_session, user_id=user1.id, max_price=Decimal("100"))
    assert len(products) == 0

def test_sorting(db_session, sample_data):
    user1 = sample_data["user1"]
    products_asc = search_dashboard_products(db_session, user_id=user1.id, sort_by_price="asc")
    assert len(products_asc) == 3
    assert products_asc[0].title == "Google Pixel 6"
    assert products_asc[1].title == "Samsung Galaxy S21"
    assert products_asc[2].title == "Apple iPhone 13"

    products_desc = search_dashboard_products(db_session, user_id=user1.id, sort_by_price="desc")
    assert len(products_desc) == 3
    assert products_desc[0].title == "Apple iPhone 13"
    assert products_desc[1].title == "Samsung Galaxy S21"
    assert products_desc[2].title == "Google Pixel 6"

    products_asc_fav = search_dashboard_products(db_session, user_id=user1.id, sort_by_price="asc", only_favorites=True)
    assert len(products_asc_fav) == 2
    assert products_asc_fav[0].title == "Google Pixel 6"
    assert products_asc_fav[1].title == "Apple iPhone 13"

    products_desc_title = search_dashboard_products(db_session, user_id=user1.id, sort_by_price="desc", title="Apple")
    assert len(products_desc_title) == 1
    assert products_desc_title[0].title == "Apple iPhone 13"

    products_asc_empty = search_dashboard_products(db_session, user_id=user1.id, sort_by_price="asc", title="NonExistent")
    assert len(products_asc_empty) == 0

def test_no_products(db_session, sample_data):
    products = search_dashboard_products(db_session, user_id=999)
    assert products == []

    user2 = sample_data["user2"]
    products = search_dashboard_products(db_session, user_id=user2.id, title="NonExisting")
    assert products == []

    products = search_dashboard_products(db_session, user_id=user2.id, title="Sony", only_favorites=True)
    assert products == []

    products = search_dashboard_products(db_session, user_id=user2.id, min_price=Decimal("1000"))
    assert products == []

    products = search_dashboard_products(db_session, user_id=user2.id, title="Apple", min_price=Decimal("1000"))
    assert products == []
