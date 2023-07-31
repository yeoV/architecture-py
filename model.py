from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set
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
    reference: str = field(alias="ref")
    sku: str
    # available_quantity: int = field(alias="qty")
    _purchased_quantity: int = field(alias="qty")
    eta: Optional[date]
    _allocations: Set[OrderLine] = set()

    # 객체 동등성을 위한  eq, hash 값
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    # sorted 를 위한 __gt__ 구현 -> eta 순 정렬
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

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


# 품절 시 에러처리할 class
class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
