import asyncio
import pytest
from decimal import Decimal
from types import SimpleNamespace
from app.parsers.amazon_parser import AmazonParser

class FakeLocator:
    def __init__(self, text=None, attr=None, children=None):
        self._text = text
        self._attr = attr
        self._children = children or {}

    async def count(self):
        return 1 if self._text or self._attr else 0

    async def inner_text(self):
        return self._text or ""

    async def get_attribute(self, name):
        return self._attr or ""

    @property
    def first(self):
        return self

    def locator(self, selector):
        if selector in self._children:
            return self._children[selector]
        return FakeLocator()

    async def all(self):
        return [self]

@pytest.fixture
def fake_item_basic():
    return FakeLocator(children={
        "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal": FakeLocator(text="Test Product"),
        "a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal": FakeLocator(attr="/test-url"),
        "img.s-image": FakeLocator(attr="http://image.url/test.jpg"),
        "span.a-price span.a-offscreen": FakeLocator(text="$123.45"),
    })

@pytest.fixture
def fake_item_missing_price():
    return FakeLocator(children={
        "h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal": FakeLocator(text="No Price Product"),
        "a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal": FakeLocator(attr="/no-price-url"),
        "img.s-image": FakeLocator(attr="http://image.url/no-price.jpg"),
    })

def test_extract_item_basic(fake_item_basic):
    parser = AmazonParser("laptop")
    result = asyncio.run(parser._extract_item(fake_item_basic))
    assert result["title"] == "Test Product"
    assert result["url"] == "https://www.amazon.co.uk//test-url"
    assert result["image_url"] == "http://image.url/test.jpg"
    assert result["price"] == "$123.45"

def test_extract_item_missing_price(fake_item_missing_price):
    parser = AmazonParser("laptop")
    result = asyncio.run(parser._extract_item(fake_item_missing_price))
    assert result["title"] == "No Price Product"
    assert result["url"] == "https://www.amazon.co.uk//no-price-url"
    assert result["image_url"] == "http://image.url/no-price.jpg"
    assert result["price"] == "N/A"
