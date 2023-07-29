from model import OneLine, Batch
from datetime import date, timedelta
import pytest

# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


# 중복된 batch와 line 만들기 코드 처리
def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        # 배치 명, 상품 명 (SKU), 갯수, 날짜
        Batch("batch-001", "SMALL-TABLE", qty=20, eta=today),
        # order 명, 상품명, 갯수
        OneLine("order-ref", "SMALL-TABLE", 2),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)
    batch.allocate(line)
    # 20 - 2 -> 18 , 아닐경우 assert
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("SMALL-TABLE", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("SMALL-TABLE", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SMALL-TABLE", 2, 2)
    assert batch.can_allocate(line)


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")
