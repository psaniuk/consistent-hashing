from datetime import datetime, timezone


def utc_now():
    return datetime.now(tz=timezone.utc)


def now_str_hh_mm_ss():
    return datetime_to_hh_mm_ss(utc_now())


def datetime_to_hh_mm_ss(dt: datetime):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def round_time(dt: datetime, tz: timezone = timezone.utc):
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0, 0, tzinfo=tz)
