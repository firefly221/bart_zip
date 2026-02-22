from lz77 import Token, compress, decompress
from format_lz77 import encode_tokens, decode_tokens
from huffman import huffman_encode, huffman_decode


def compress_file(in_path: str, out_path: str) -> None:
    data = open(in_path, "rb").read()

    tokens = compress(data)
    raw = encode_tokens(tokens, orig_len=len(data))
    blob = huffman_encode(raw)

    open(out_path, "wb").write(blob)


def decompress_file(in_path: str, out_path: str) -> None:
    blob = open(in_path, "rb").read()

    raw = huffman_decode(blob)
    tokens, orig_len = decode_tokens(raw)

    data = decompress(tokens)
    if len(data) != orig_len:
        raise ValueError("length mismatch")

    open(out_path, "wb").write(data)