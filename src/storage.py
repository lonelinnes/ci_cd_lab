class Storage:
    def __init__(self):
        self.catalog = {"coffee": 150.0, "tea": 100.0, "cake": 200.0}
        self.reservations = 0

    def get_price(self, product: str) -> float:
        if product not in self.catalog:
            raise KeyError(f"Товар '{product}' не найден в каталоге")
        return self.catalog[product]

    def create_reservation(self) -> str:
        self.reservations += 1
        return f"RES-{self.reservations:04d}"