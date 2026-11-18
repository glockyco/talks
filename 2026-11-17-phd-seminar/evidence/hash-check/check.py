"""Can Z3 find an input that reaches `return true` in a SHA-256 password check?

The path condition of that return is SHA-256(password) == STORED. The script encodes
SHA-256 over bit vectors for a password of eight unknown bytes and asks Z3 for a model.
A first query fixes the bytes to the real password, to show that the encoding is right.
"""
import hashlib
import sys
import time

import z3

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
H0 = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def rotr(x, n):
    return z3.RotateRight(x, n)


def sha256_block(words):
    w = list(words)
    for i in range(16, 64):
        s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ z3.LShR(w[i - 15], 3)
        s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ z3.LShR(w[i - 2], 10)
        w.append(w[i - 16] + s0 + w[i - 7] + s1)
    a, b, c, d, e, f, g, h = [z3.BitVecVal(v, 32) for v in H0]
    for i in range(64):
        s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        t1 = h + s1 + ch + z3.BitVecVal(K[i], 32) + w[i]
        s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = s0 + maj
        h, g, f, e, d, c, b, a = g, f, e, d + t1, c, b, a, t1 + t2
    return [z3.BitVecVal(v, 32) + x for v, x in zip(H0, [a, b, c, d, e, f, g, h])]


def query(password: bytes, fixed: bool, timeout_s: int):
    n = len(password)
    data = [z3.BitVec(f"c{i}", 8) for i in range(n)]
    # One block: the message, 0x80, zeros, and the length in bits.
    block = data + [z3.BitVecVal(0x80, 8)] + [z3.BitVecVal(0, 8)] * (55 - n) + [z3.BitVecVal(n * 8, 64)]
    flat = z3.Concat(*block)
    words = [z3.Extract(511 - 32 * i, 480 - 32 * i, flat) for i in range(16)]
    digest = sha256_block(words)
    stored = hashlib.sha256(password).digest()
    solver = z3.Solver()
    solver.set("timeout", timeout_s * 1000)
    for i, word in enumerate(digest):
        solver.add(word == int.from_bytes(stored[4 * i:4 * i + 4], "big"))
    if fixed:
        for c, v in zip(data, password):
            solver.add(c == v)
    start = time.time()
    result = solver.check()
    took = time.time() - start
    reason = solver.reason_unknown() if result == z3.unknown else ""
    return result, took, reason


if __name__ == "__main__":
    timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    print("z3", z3.get_version_string())
    print("password fixed to the real one:", query(b"hunter22", True, 60))
    print(f"password unknown, timeout {timeout} s:", query(b"hunter22", False, timeout))
