from dataclasses import dataclass
from datetime import date
from typing import Optional, Set
from attrs import define, field


# 동작이 없는 불변 class
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


# 동적으로 변하는 값은 init 함수 만드는게 좋을 지도
# ㄴㄴ attrs 로 해결
@define
class Batch:
    ref: str
    sku: str
    # available_quantity: int = field(alias="qty")
    _purchased_quantity: int = field(alias="qty")
    eta: Optional[date]
    _allocations: Set[OrderLine] = set()

    # 엔티티 정체성 동등성 구현

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    # test 를 위한 func
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
