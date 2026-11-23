
import time
import uuid

from app.core.ids import new_id


def test_generated_id_is_uuid_v7():
    generated_id = new_id()

    assert isinstance(generated_id, uuid.UUID)
    assert generated_id.version == 7


def test_timestamp_is_present_in_uuid():
    before = int(time.time() * 1000)

    generated_id = new_id()

    after = int(time.time() * 1000)

    timestamp = int.from_bytes(generated_id.bytes[:6], "big")

    assert before <= timestamp <= after


def test_ids_follow_time_order():
    first_id = new_id()

    # Wait until the next millisecond.
    time.sleep(0.005)

    second_id = new_id()

    assert first_id.int < second_id.int


def test_1000_ids_are_unique():
    generated_ids = {new_id() for _ in range(1000)}

    assert len(generated_ids) == 1000