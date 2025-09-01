from pydantic import BaseModel, HttpUrl, ConfigDict, condecimal
from datetime import datetime
from typing import List, Optional

class PriceBase(BaseModel):
    site: str
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    date: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    title: str
    url: HttpUrl
    image_url: HttpUrl

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    prices: List[Price] = []
    
    model_config = ConfigDict(from_attributes=True)