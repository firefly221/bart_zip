from lz77 import *
from format_huffman import *


data = open("nether.png", "rb").read()

# pipeline ręczny
tokens = compress(data)
raw = encode_tokens(tokens, len(data))
packed = huffman_encode(raw)

raw2 = huffman_decode(packed)
tokens2, orig_len = decode_tokens(raw2)
data2 = decompress(tokens2)

print(data == data2)