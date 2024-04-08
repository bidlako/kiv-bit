import random
import logging

logger = logging.getLogger(__name__)

KEY_SIZE = 250
WEIGHT_INTERVAL = 100, 400
Q_INTERVAL = 100, 200


def generate_p():
    return 0x100




def generate_private_key(p, q) -> [int]:
    logging.debug(f"Generating private key with size {KEY_SIZE}.")
    private_key = []
    while len(private_key) < KEY_SIZE:
        item = gen_item()
        if is_super_increasing(private_key + [item]):
            private_key.append(item)
    return private_key


def generate_public_key(p, q, private_key) -> int:
    return sum(private_key) % (p * q)


def generate_q():
    return gen_bits_from_interval(Q_INTERVAL)

def gen_item() -> int:
    return gen_bits_from_interval(WEIGHT_INTERVAL)


def gen_bits_from_interval(interval: tuple[int, int]) -> int:
    size = random.randint(*interval)
    return random.getrandbits(size)


def is_super_increasing(items):
    return all(sum(items[:i]) > items[i] for i in range(1, len(items)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    p = generate_p()
    q = generate_q()

    private_key = generate_private_key(p, q)
    assert is_super_increasing(private_key) is True

    public_key = generate_public_key(p, q, private_key)
    print(f"p: {p}")
    print(f"q: {q}")
    print(f"private_key: {private_key}")
    print(f"public_key: {public_key}")
