import os
import random

from lz77 import compress, decompress
from format_lz77 import encode_tokens, decode_tokens



def roundtrip_bytes(x: bytes) -> None:
    tokens = compress(x)
    y = decompress(tokens)
    assert y == x

def roundtrip_encoded(x: bytes) -> None:
    tokens = compress(x)
    blob = encode_tokens(tokens, orig_len=len(x))
    tokens2, orig_len2 = decode_tokens(blob)
    y = decompress(tokens2)
    assert orig_len2 == len(x)
    assert y == x

def test_small_cases():
    cases = [
        b"",
        b"a",
        b"abracadabra!",
        b"a" * 10000,
        b"abc" * 5000,
    ]
    for x in cases:
        roundtrip_bytes(x)
        roundtrip_encoded(x)

def test_random_cases():
    for _ in range(200):
        x = os.urandom(random.randint(0, 5000))
        roundtrip_bytes(x)
        roundtrip_encoded(x)