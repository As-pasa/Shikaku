def get_divider_pairs(x: int) -> (tuple[int, int]):
    for i in range(1, x + 1):
        if x % i == 0:
            yield i, x // i
