from pydantic import BaseModel
import json
from datetime import datetime
from database import write_account, read_account, write_log

INITIAL_STOCK = 20


class Car(BaseModel):
    model: str
    price: float


class Transaction(BaseModel):
    model: str
    quantity: int
    price: float
    timestamp: str
    action: str  # "buy", "sell", "maintenance"

    def total(self) -> float:
        return self.quantity * self.price

    def __repr__(self):
        return f"{abs(self.quantity)} {self.model}(s) at {self.price} each [{self.action}]"


class CarShowroom(BaseModel):
    name: str
    balance: float
    inventory: dict[str, int]
    maintenance: dict[str, int]
    transactions: list[Transaction]
    showroom_value_time_series: list[tuple[str, float]]
    def list_transactions(self):
        return [t.model_dump() for t in self.transactions]
    @classmethod
    def get(cls, name: str):
        fields = read_account(name.lower())
        if not fields:
            fields = {
                "name": name.lower(),
                "balance": 0.0,
                "inventory": {},
                "maintenance": {},
                "transactions": [],
                "showroom_value_time_series": []
            }
            write_account(name, fields)
        return cls(**fields)

    def save(self):
        write_account(self.name.lower(), self.model_dump())

    def add_stock(self, model: str, quantity: int, price: float):
        """Add new cars to inventory"""
        self.inventory[model] = self.inventory.get(model, 0) + quantity

        transaction = Transaction(
            model=model,
            quantity=quantity,
            price=price,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action="buy"
        )

        self.transactions.append(transaction)
        self.save()
        write_log(self.name, "showroom", f"Added {quantity} {model}")

    def sell_car(self, model: str, quantity: int, price: float):
        """Sell cars if available"""
        if self.inventory.get(model, 0) < quantity:
            raise ValueError("Not enough cars in stock")

        self.inventory[model] -= quantity

        if self.inventory[model] == 0:
            del self.inventory[model]

        self.balance += price * quantity

        transaction = Transaction(
            model=model,
            quantity=-quantity,
            price=price,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action="sell"
        )

        self.transactions.append(transaction)
        self.save()
        write_log(self.name, "showroom", f"Sold {quantity} {model}")

    def send_to_maintenance(self, model: str, quantity: int):
        """Move cars to maintenance"""
        if self.inventory.get(model, 0) < quantity:
            raise ValueError("Not enough cars in inventory")

        self.inventory[model] -= quantity
        self.maintenance[model] = self.maintenance.get(model, 0) + quantity

        transaction = Transaction(
            model=model,
            quantity=quantity,
            price=0,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action="maintenance"
        )

        self.transactions.append(transaction)
        self.save()
        write_log(self.name, "showroom", f"{quantity} {model} sent to maintenance")

    def return_from_maintenance(self, model: str, quantity: int):
        """Return cars from maintenance to inventory"""
        if self.maintenance.get(model, 0) < quantity:
            raise ValueError("Not enough cars in maintenance")

        self.maintenance[model] -= quantity
        self.inventory[model] = self.inventory.get(model, 0) + quantity

        self.save()
        write_log(self.name, "showroom", f"{quantity} {model} returned from maintenance")

    def calculate_showroom_value(self):
        """Calculate total showroom value"""
        total = self.balance

        for model, qty in self.inventory.items():
            total += qty * 10000  # assumed base price

        for model, qty in self.maintenance.items():
            total += qty * 8000  # depreciated value

        return total

    def report(self):
        value = self.calculate_showroom_value()
        self.showroom_value_time_series.append(
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), value)
        )

        self.save()

        data = self.model_dump()
        data["total_value"] = value

        write_log(self.name, "showroom", "Generated report")
        return json.dumps(data, indent=2)


# Example usage
if __name__ == "__main__":
    showroom = CarShowroom.get("Elite Motors")

    showroom.add_stock("Tesla Model S", 5, 80000)
    showroom.add_stock("BMW X5", 3, 60000)

    showroom.sell_car("Tesla Model S", 2, 85000)

    showroom.send_to_maintenance("BMW X5", 1)
    showroom.return_from_maintenance("BMW X5", 1)

    print(showroom.report())