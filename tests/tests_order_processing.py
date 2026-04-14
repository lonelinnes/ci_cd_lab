import pytest
import logging
from src.service import process_order
from src.storage import Storage

@pytest.fixture
def storage(): return Storage()

@pytest.fixture
def logger(): return logging.getLogger("test")

def test_success_order(storage, logger):
    res = process_order("alice, coffee, 2", storage, logger)
    assert res.user == "alice"
    assert res.qty == 2
    assert res.amount == 300.0  # 150 * 2

def test_qty_zero_or_negative(storage, logger):
    with pytest.raises(ValueError, match="должно быть > 0"):
        process_order("bob, tea, 0", storage, logger)

def test_unknown_product(storage, logger):
    with pytest.raises(KeyError, match="не найден в каталоге"):
        process_order("kate, pizza, 1", storage, logger)