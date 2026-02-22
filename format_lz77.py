import struct
from lz77 import *



MAGIC = b"LZ77"

def encode_tokens(tokens: list[Token], orig_len: int) -> bytes:
    out = bytearray()
    out += MAGIC
    out += struct.pack("<II", orig_len, len(tokens))

    for t in tokens:
        has_next = 1 if (t.nextChar is not None and t.nextChar != b"") else 0
        nxt = t.nextChar[0] if has_next else 0
        out += struct.pack("<HBBB", t.offset, t.length, has_next, nxt)

    return bytes(out)

def decode_tokens(blob: bytes) -> tuple[list[Token], int]:
    if len(blob) < 12 or blob[:4] != MAGIC:
        raise ValueError("bad header")

    orig_len, count = struct.unpack_from("<II", blob, 4)
    pos = 12
    need = pos + count * 5
    if len(blob) < need:
        raise ValueError("truncated")

    tokens: list[Token] = []
    for _ in range(count):
        offset, length, has_next, nxt = struct.unpack_from("<HBBB", blob, pos)
        pos += 5
        nextChar = bytes([nxt]) if has_next else b""
        tokens.append(Token(offset=offset, length=length, nextChar=nextChar))

    return tokens, orig_len

def compress_file(in_path: str, out_path: str) -> None:
    data = open(in_path, "rb").read()
    tokens = compress(data)
    blob = encode_tokens(tokens, orig_len=len(data))
    open(out_path, "wb").write(blob)

def decompress_file(in_path: str, out_path: str) -> None:
    blob = open(in_path, "rb").read()
    tokens, orig_len = decode_tokens(blob)
    data = decompress(tokens)
    if len(data) != orig_len:
        raise ValueError("length mismatch")
    open(out_path, "wb").write(data)
