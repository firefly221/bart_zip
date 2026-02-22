import struct
import heapq
from dataclasses import dataclass
from typing import Optional


MAGIC = b"HUFF"  


@dataclass
class _Node:
    freq: int
    sym: Optional[int] = None
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


class _BitWriter:
    def __init__(self) -> None:
        self.out = bytearray()
        self.cur = 0
        self.nbits = 0  

    def write_bits(self, bits: int, bitlen: int) -> None:
       
        for k in range(bitlen - 1, -1, -1):
            b = (bits >> k) & 1
            self.cur = (self.cur << 1) | b
            self.nbits += 1
            if self.nbits == 8:
                self.out.append(self.cur)
                self.cur = 0
                self.nbits = 0

    def finish(self) -> bytes:
        if self.nbits:
            
            self.cur <<= (8 - self.nbits)
            self.out.append(self.cur)
            self.cur = 0
            self.nbits = 0
        return bytes(self.out)


class _BitReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0
        self.cur = 0
        self.nbits = 0

    def read_bit(self) -> int:
        if self.nbits == 0:
            if self.pos >= len(self.data):
                raise ValueError("truncated bitstream")
            self.cur = self.data[self.pos]
            self.pos += 1
            self.nbits = 8
        self.nbits -= 1
        return (self.cur >> self.nbits) & 1


def _build_tree(freq: list[int]) -> Optional[_Node]:
    heap: list[tuple[int, int, _Node]] = []
    uid = 0

    for s in range(256):
        if freq[s] > 0:
            heapq.heappush(heap, (freq[s], uid, _Node(freq=freq[s], sym=s)))
            uid += 1

    if not heap:
        return None

 
    if len(heap) == 1:
        return heap[0][2]

    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        parent = _Node(freq=f1 + f2, left=a, right=b)
        heapq.heappush(heap, (parent.freq, uid, parent))
        uid += 1

    return heap[0][2]


def _build_codes(root: _Node) -> list[tuple[int, int]]:
    
    codes: list[tuple[int, int]] = [(0, 0)] * 256

    if root.sym is not None:
        
        codes[root.sym] = (0, 1)
        return codes

    def dfs(node: _Node, bits: int, bitlen: int) -> None:
        if node.sym is not None:
            codes[node.sym] = (bits, bitlen)
            return
        # lewo = 0, prawo = 1
        if node.left is not None:
            dfs(node.left, (bits << 1), bitlen + 1)
        if node.right is not None:
            dfs(node.right, (bits << 1) | 1, bitlen + 1)

    dfs(root, 0, 0)
    return codes


def huffman_encode(data: bytes) -> bytes:
    
    orig_len = len(data)

    freq = [0] * 256
    for b in data:
        freq[b] += 1

    root = _build_tree(freq)

    out = bytearray()
    out += MAGIC
    out += struct.pack("<I", orig_len)
    out += struct.pack("<256I", *freq)

    if orig_len == 0:
        return bytes(out)

    if root is None:
        raise ValueError("internal: empty tree for non-empty data")

    codes = _build_codes(root)
    bw = _BitWriter()

    for b in data:
        bits, bitlen = codes[b]
        bw.write_bits(bits, bitlen)

    out += bw.finish()
    return bytes(out)


def huffman_decode(blob: bytes) -> bytes:
    if len(blob) < 4 + 4 + 256 * 4:
        raise ValueError("truncated header")
    if blob[:4] != MAGIC:
        raise ValueError("bad magic")

    orig_len = struct.unpack_from("<I", blob, 4)[0]
    freq = list(struct.unpack_from("<256I", blob, 8))
    bitstream = blob[8 + 256 * 4 :]

    if orig_len == 0:
        return b""

    root = _build_tree(freq)
    if root is None:
        raise ValueError("bad freq table (empty)")

   
    if root.sym is not None:
        return bytes([root.sym]) * orig_len

    br = _BitReader(bitstream)
    out = bytearray()

    node = root
    while len(out) < orig_len:
        bit = br.read_bit()
        node = node.right if bit else node.left
        if node is None:
            raise ValueError("bad bitstream")
        if node.sym is not None:
            out.append(node.sym)
            node = root

    return bytes(out)