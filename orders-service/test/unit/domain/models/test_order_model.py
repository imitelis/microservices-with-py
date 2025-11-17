import pytest
from pydantic import ValidationError
from src.domain.models.order import Order

def test_order_creation_with_all_fields():
    order = Order(id=1, item="Laptop", quantity=2)
    assert order.id == 1
    assert order.item == "Laptop"
    assert order.quantity == 2

def test_order_creation_without_id():
    order = Order(item="Mouse", quantity=1)
    assert order.id is None
    assert order.item == "Mouse"
    assert order.quantity == 1

def test_order_creation_missing_required_fields():
    with pytest.raises(ValidationError) as exc_info:
        Order()
    
    errors = exc_info.value.errors()
    assert len(errors) == 2  # Missing 'item' and 'quantity'
    assert any(error['loc'] == ('item',) for error in errors)
    assert any(error['loc'] == ('quantity',) for error in errors)

def test_order_creation_missing_item():
    with pytest.raises(ValidationError) as exc_info:
        Order(quantity=1)
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('item',)

def test_order_creation_missing_quantity():
    with pytest.raises(ValidationError) as exc_info:
        Order(item="Keyboard")
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('quantity',)

def test_order_serialization():
    order = Order(id=1, item="Monitor", quantity=2)
    order_dict = order.model_dump()
    
    assert order_dict == {
        "id": 1,
        "item": "Monitor",
        "quantity": 2
    }

def test_order_json_serialization():
    order = Order(id=1, item="Headphones", quantity=1)
    json_str = order.model_dump_json()
    
    assert '"id":1' in json_str
    assert '"item":"Headphones"' in json_str
    assert '"quantity":1' in json_str

def test_order_equality():
    order1 = Order(id=1, item="Tablet", quantity=1)
    order2 = Order(id=1, item="Tablet", quantity=1)
    order3 = Order(id=2, item="Tablet", quantity=1)
    
    assert order1 == order2
    assert order1 != order3

def test_order_with_invalid_quantity_type():
    with pytest.raises(ValidationError) as exc_info:
        Order(item="Phone", quantity="invalid")
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('quantity',)
    assert 'int_parsing' in errors[0]['type']