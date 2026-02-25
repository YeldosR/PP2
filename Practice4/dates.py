from datetime import datetime, timedelta


def minus_five_days():
    return datetime.now() - timedelta(days=5)


def day_triplet():
    today = datetime.now()
    return (
        today - timedelta(days=1),
        today,
        today + timedelta(days=1)
    )


def drop_microseconds(dt):
    return dt.replace(microsecond=0)


def diff_seconds(d1, d2):
    return abs((d2 - d1).total_seconds())


if __name__ == "__main__":
    print("Minus 5:", minus_five_days())

    y, t, tm = day_triplet()
    print("Yesterday:", y)
    print("Today:", t)
    print("Tomorrow:", tm)

    now = datetime.now()
    print("No micro:", drop_microseconds(now))

    d1 = datetime(2024, 1, 1)
    d2 = datetime(2024, 1, 2)
    print("Seconds diff:", diff_seconds(d1, d2))