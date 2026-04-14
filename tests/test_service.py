import pytest
import logging
from src.service import process_order
from src.storage import Storage


@pytest.fixture
def storage():
    return Storage()


@pytest.fixture
def logger():
    return logging.getLogger("test")


def test_process_ok(storage, logger):
    """Тест на нормальный сценарий"""
    result = process_order("alice, coffee, 2", storage, logger)

    assert result.user == "alice"
    assert result.product == "coffee"
    assert result.qty == 2
    assert result.amount == 300.0  # ✅ Исправлено: было 360, должно быть 300.0
    assert result.reserve_id is not None