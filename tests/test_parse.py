import pytest
import logging
from src.service import process_order  # ✅ Правильное имя функции!
from src.storage import Storage

@pytest.fixture
def storage():
    return Storage()

@pytest.fixture
def logger():
    return logging.getLogger("test")

def test_parse_ok(storage, logger):
    """Тест 1: нормальный заказ"""
    result = process_order("alice, coffee, 2", storage, logger)
    assert result.user == "alice"
    assert result.product == "coffee"
    assert result.qty == 2
    assert result.amount == 300.0  # 150 * 2

def test_parse_invalid_qty(storage, logger):
    """Тест 2: qty=0 (баг из задания)"""
    with pytest.raises(ValueError, match="должно быть > 0"):
        process_order("bob, tea, 0", storage, logger)