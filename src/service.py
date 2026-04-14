from dataclasses import dataclass
import logging


@dataclass
class OrderResult:
    user: str
    product: str
    qty: int
    amount: float
    reserve_id: str


def process_order(raw: str, storage, logger: logging.Logger) -> OrderResult:
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 3:
        raise ValueError(f"Ошибка парсинга: ожидается 3 поля, получено {len(parts)}")

    user, product, qty_str = parts
    logger.info(f"Начало обработки | user={user} | raw='{raw}'")

    try:
        qty = int(qty_str)
    except ValueError:
        raise ValueError(f"Количество должно быть числом, получено '{qty_str}'")

    if qty <= 0:
        raise ValueError(f"Количество должно быть > 0, получено {qty}")

    price = storage.get_price(product)
    amount = price * qty
    reserve_id = storage.create_reservation()

    logger.info(f"Заказ успешен | user={user} | amount={amount}")
    return OrderResult(user=user, product=product, qty=qty, amount=amount, reserve_id=reserve_id)