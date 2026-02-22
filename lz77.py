from dataclasses import dataclass


@dataclass
class Token:
    offset: int
    length: int
    nextChar: bytes


def compress(data: bytes) -> list[Token]:
   
    WINDOW = 2048
    MIN_MATCH = 3
    MAX_MATCH = 255

    
    HASH_BITS = 16
    HASH_SIZE = 1 << HASH_BITS
    HASH_MASK = HASH_SIZE - 1
    CHAIN_LIMIT = 32 

    mv = memoryview(data)
    dataLen = len(mv)


    buckets: list[list[int]] = [[] for _ in range(HASH_SIZE)]

    def h3(pos: int) -> int:
        
        return ((mv[pos] << 16) ^ (mv[pos + 1] << 8) ^ mv[pos + 2]) & HASH_MASK

    tokens: list[Token] = []
    i = 0

    while i < dataLen:
        bestLen = 0
        bestOff = 0

        windowStart = max(0, i - WINDOW)

        
        if i + MIN_MATCH <= dataLen:
            hh = h3(i)
            cand_list = buckets[hh]

          
            k0 = 0
            while k0 < len(cand_list) and cand_list[k0] < windowStart:
                k0 += 1
            if k0:
                del cand_list[:k0]

         
            checked = 0
            for j in reversed(cand_list):
             
                l = 0
                
                while (
                    l < MAX_MATCH
                    and i + l < dataLen
                    and j + l < i
                    and mv[j + l] == mv[i + l]
                ):
                    l += 1

                if l > bestLen:
                    bestLen = l
                    bestOff = i - j
                    if bestLen == MAX_MATCH:
                        break

                checked += 1
                if checked >= CHAIN_LIMIT:
                    break

        if bestLen >= MIN_MATCH:
            nxt_i = i + bestLen
            nextChar = mv[nxt_i:nxt_i + 1].tobytes()  
            tokens.append(Token(offset=bestOff, length=bestLen, nextChar=nextChar))


            end = min(nxt_i + 1, dataLen)  
            pos = i
            while pos + MIN_MATCH <= dataLen and pos < end:
                buckets[h3(pos)].append(pos)
                pos += 1

            i = nxt_i + (1 if nxt_i < dataLen else 0)
        else:
            # literal
            tokens.append(Token(offset=0, length=0, nextChar=mv[i:i + 1].tobytes()))

            
            if i + MIN_MATCH <= dataLen:
                buckets[h3(i)].append(i)

            i += 1

    return tokens


def decompress(tokenList: list[Token]) -> bytes:
    out = bytearray()

    for token in tokenList:
        if token.offset == 0 and token.length == 0:
            out.extend(token.nextChar)
            continue

        start = len(out) - token.offset

        
        if token.offset >= token.length:
            out.extend(out[start:start + token.length])
        else:
            for k in range(token.length):
                out.append(out[start + k])

        if token.nextChar:
            out.extend(token.nextChar)

    return bytes(out)