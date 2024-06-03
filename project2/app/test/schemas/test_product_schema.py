import pytest
from app.schemas.product import Product,ProductInput,ProductOutput
from app.schemas.category import Category



def test_product_schema():
    products=Product(
        name="Camisa myke",
        slug="camisa-myke",
        price=29.99,
        stock=1 
    )

    assert products.dict()=={
        "name":"Camisa myke",
        "slug":"camisa-myke",
        "price":29.99,
        "stock":1 

    }

def test_invalid_product_schema():
    with pytest.raises(ValueError):
        products=Product(
            name="Camisa myke",
            slug="camisa myke",
            price=29.99,
            stoc=1
        )
    
    with pytest.raises(ValueError):
        products=Product(
            name="Camisa myke",
            slug="Camisa-myke",
            price=29.99,
            stock=1
        )

    with pytest.raises(ValueError):
        products=Product(
            name="Camisa myke",
            slug="cãmisa-myke",
            price=29.99,
            stock=1
        )
    
    with pytest.raises(ValueError):
        products=Product(
            name="Camisa myke",
            slug="camisa-myke",
            price=0,
            stock=1
        )


def test_product_input_schema():
    product=Product(
        name="Camisa Myke",
        slug="camisa-myke",
        price=22.99,
        stock=22
    )
        
    product_input = ProductInput(
         category_slug="roupa",
         product=product
         )
    assert product_input.dict() == {
        "category_slug": "roupa",
        "product":{"name": "Camisa Myke",
                   "slug":"camisa-myke",
                   "price":22.99,
                   "stock":22
        }
    }


def test_product_output_schema():
    category = Category(name="Roupa",slug="roupa")

    product_output = ProductOutput(
        id=1,
        name="Camisa",
        slug="camisa",
        price=10,
        stock=10,
        category=category
    )

    assert product_output.dict() == {
        "id":1,
        "name":"Camisa",
        "slug":"camisa",
        "price": 10,
        "stock":10,
        "category": {
            "name":"Roupa",
            "slug":"roupa"
        }
    }