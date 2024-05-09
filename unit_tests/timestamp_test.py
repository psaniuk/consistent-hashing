from app.timestamp import *
from datetime import datetime, timezone


class TestTimestamp:
    def test_now_hh_mm_ss(self):
        now = now_str_hh_mm_ss()
        assert now == str(datetime.now(tz=timezone.utc)).split(".")[0]

    def test_utc_now(self):
        assert utc_now is not None
