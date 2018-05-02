
def increase_timeout_fibonacci():
    y = 1
    x = 0
    while True:
        z = x + y
        x = y
        y = z
        if (x > 300):
            x = 300
        yield x


def increase_timeout_linear():
    x = 0
    while True:
        x += 1
        yield x
