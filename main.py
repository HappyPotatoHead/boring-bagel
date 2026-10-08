# one type of item
# operations related to that one specific item
# ordering

import time
from datetime import datetime, timezone
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class OrderStatus(Enum):
    TODO = "todo"
    PREPARING = "preparing"
    COMPLETED = "completed"

    def __str__(self) -> str:
        return self.value


# Basic item
class Item(BaseModel):
    item_id: int
    name: str = Field(min_length=5, max_length=25)
    description: str = Field(min_length=10, max_length=100)
    price: int = Field(gt=0)

    def __str__(self) -> str:
        return f"{self.name} {self.description} RM {self.price}"


# this will be conveted into a table (FastAPI)
class Order(BaseModel):
    order_id: int = Field(default_factory=lambda: Order._retrieve_next_order_id())
    order_status: OrderStatus = OrderStatus.TODO
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    update_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    paid: bool = False

    _next_order_id: ClassVar[int] = 1

    @classmethod
    def _retrieve_next_order_id(cls):
        order_id = cls._next_order_id
        cls._next_order_id += 1
        return order_id

    def __str__(self) -> str:
        return (
            f"Order_id: {self.order_id}, status: {self.order_status}, paid: {self.paid}"
        )


class OrderItems(BaseModel):
    order_item_id: int = Field(
        default_factory=lambda: OrderItems._retrieve_next_order_id()
    )
    order_id: int
    item_id: int
    quantity: int = Field(ge=1, le=100)
    price: int = Field(gt=0)

    _next_order_id: ClassVar[int] = 1

    @classmethod
    def _retrieve_next_order_id(cls):
        order_id = cls._next_order_id
        cls._next_order_id += 1
        return order_id


# one customer -> a lot of orders
# one order -> a lot of items
# product -> a lot of orders
# order_items between product and order

items: dict[int, Item] = {
    1: Item(
        item_id=1,
        description="caffeine for your sleep deprived body",
        name="coffee",
        price=5,
    ),
    2: Item(
        item_id=2, description="bagel to go with your coffee", name="bagel", price=8
    ),
}

orders: dict[int, Order] = {}
orders_statuses: dict[OrderStatus, set[int]] = {
    OrderStatus.TODO: set(),
    OrderStatus.PREPARING: set(),
    OrderStatus.COMPLETED: set(),
}

order_items: dict[int, OrderItems] = {}


def list_orders(status: OrderStatus | None = None):
    if status is None:
        for order in orders.values():
            print(order)

        return

    for id in orders_statuses[status]:
        print(orders[id])


def create_order(item_id: int, quantity: int):
    order = Order()
    price_per_item = items[item_id].price
    order_item = OrderItems(
        order_id=order.order_id,
        item_id=item_id,
        quantity=quantity,
        price=price_per_item * quantity,
    )

    orders[order.order_id] = order
    orders_statuses[order.order_status].add(order.order_id)
    order_items[order_item.order_item_id] = order_item

    return order


def update_order(order_id: int, order_status: OrderStatus):
    order = orders.get(order_id)

    if order is None:
        raise ValueError(f"This order {order_id} does not exist!")

    orders_statuses[order.order_status].remove(order_id)
    order.order_status = order_status
    order.update_date = datetime.now(timezone.utc)

    orders_statuses[order_status].add(order_id)


def delete_order(order_id: int):
    order = orders.get(order_id)
    if order is None:
        raise ValueError(f"This order {order_id} does not exist!")
    del orders[order_id]
    orders_statuses[order.order_status].remove(order_id)


def main():
    print("Welcome!")
    print("what do you want to order?")
    print("Items")
    print("1. Coffee \n2. Bagel")
    item_id = int(input("Item: "))
    quantity = int(input("Quantity: "))
    order = create_order(item_id, quantity)
    print(order)
    print(orders)

    update_order(order.order_id, OrderStatus.PREPARING)
    print(orders)
    print(orders_statuses)
    print()
    time.sleep(3)

    update_order(order.order_id, OrderStatus.COMPLETED)
    print(orders)
    print(orders_statuses)
    print()
    time.sleep(3)

    delete_order(order.order_id)
    print(orders)
    print(orders_statuses)
    print()


if __name__ == "__main__":
    main()
