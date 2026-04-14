from src.version import version
from src.logger import setup_logger
from src.storage import Storage
from src.service import process_order
import traceback

def main():
    logger = setup_logger()
    storage = Storage()
    print(f"Maintenance Lab v{version}")
    print("-" * 50)

    orders = [
        "alice, coffee, 2",
        "bob, tea, 1",
        "kate, pizza, 1",       # Баг 2: неизвестный товар
        "john, coffee, two",    # Баг 1: нечисловое количество
        "eva, tea, 0",          # Баг 3: qty=0
    ]

    results = {'success': 0, 'failed': 0, 'errors': []}

    for idx, raw in enumerate(orders, 1):
        print(f"\n[{idx}] Обработка: {raw}")
        try:
            result = process_order(raw, storage, logger)
            print(f"УСПЕХ: {result.user} купил {result.qty} x {result.product}")
            print(f"   Сумма: {result.amount} руб.")
            print(f"   Резерв: {result.reserve_id}")
            results['success'] += 1
        except ValueError as e:
            results['failed'] += 1
            results['errors'].append({'order': raw, 'type': 'validation_error', 'message': str(e)})
            logger.error(f"Ошибка валидации | raw='{raw}' | msg={e}")
            print(f"ОШИБКА ВАЛИДАЦИИ: {e}")
        except KeyError as e:
            results['failed'] += 1
            results['errors'].append({'order': raw, 'type': 'product_not_found', 'message': str(e)})
            logger.error(f"Товар не найден | raw='{raw}' | msg={e}")
            print(f"ОШИБКА: Товар отсутствует в каталоге")
        except Exception as e:
            results['failed'] += 1
            results['errors'].append({'order': raw, 'type': 'unexpected', 'message': str(e)})
            logger.critical(f"Неожиданная ошибка | raw='{raw}' | {traceback.format_exc()}")
            print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")

    print("\n" + "=" * 50)
    print("ИТОГОВЫЙ ОТЧЕТ")
    print(f"Успешно обработано: {results['success']}")
    print(f"Ошибок: {results['failed']}")
    if results['errors']:
        print("\nДетали ошибок:")
        for err in results['errors']:
            print(f"  - Заказ: {err['order']} | Тип: {err['type']} | Сообщение: {err['message']}")

if __name__ == "__main__":
    main()