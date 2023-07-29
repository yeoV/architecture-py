from dataclasses import dataclass
from datetime import date
from typing import Optional
from attrs import define, field


# 동작이 없는 불변 class
@dataclass(frozen=True)
class OneLine:
    orderid: str
    sku: str
    qty: int


# 동적으로 변하는 값은 init 함수 만드는게 좋을 지도
# ㄴㄴ attrs 로 해결
@define
class Batch:
    ref: str
    sku: str
    available_quantity: int = field(alias="qty")
    eta: Optional[date]

    # def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
    #     self.ref = ref
    #     self.sku = sku
    #     self.available_quantity = qty
    #     self.eta = eta

    def allocate(self, line: OneLine):
        self.available_quantity -= line.qty

    # test 를 위한 func
    def can_allocate(self, line: OneLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
