import base64

def int32(n):
    return n & 0xFFFFFFFF

# 1. Exact Mulberry32 implementation from the JS source
def mulberry32(seed):
    state = seed
    def next_val():
        nonlocal state
        state = int32(state + 0x6D2B79F5)
        t = int32(state ^ (state >> 15))
        t = int32(t * (t | 1))
        # JS: t ^= t + Math.imul(t ^ t >>> 7, t | 61);
        # Precedence: t = t ^ (t + imul)
        m = int32((t ^ (t >> 7)) * (t | 61))
        t = int32(t ^ int32(t + m))
        return int32(t ^ (t >> 14)) / 4294967296
    return next_val

# 2. Custom SHA256 implementation replicating the "chaining" bug in the HTML
class CustomSHA256:
    def __init__(self):
        self.h = []
        self.k = []
        self.init_constants()

    def init_constants(self):
        prime_counter = 0
        is_composite = [False] * 313
        candidate = 2
        while prime_counter < 64:
            if not is_composite[candidate]:
                for i in range(candidate * candidate, 313, candidate):
                    is_composite[i] = True
                self.h.append(int(pow(candidate, 0.5) * 0x100000000) & 0xFFFFFFFF)
                self.k.append(int(pow(candidate, 1/3) * 0x100000000) & 0xFFFFFFFF)
                prime_counter += 1
            candidate += 1

    def rotate_right(self, v, n):
        return ((v >> n) | (v << (32 - n))) & 0xFFFFFFFF

    def hash(self, ascii_str):
        ascii_bit_length = len(ascii_str) * 8
        ascii_bytes = bytearray(ascii_str, 'ascii')
        
        # Padding logic from the JS
        ascii_bytes.append(0x80)
        while (len(ascii_bytes) % 64) != 56:
            ascii_bytes.append(0x00)
        
        # Convert bytes to 32-bit words (Big Endian)
        words = []
        for i in range(0, len(ascii_bytes), 4):
            w = (ascii_bytes[i] << 24) | (ascii_bytes[i+1] << 16) | (ascii_bytes[i+2] << 8) | ascii_bytes[i+3]
            words.append(w)
        
        # Append length (64-bit)
        words.append(0) # High 32 bits
        words.append(ascii_bit_length) # Low 32 bits
        
        # The JS code uses self.h as the starting point (chaining)
        current_h = self.h[:8]
        
        for j in range(0, len(words), 16):
            w = words[j:j+16]
            old_h = current_h[:]
            
            # Message schedule expansion
            for i in range(16, 64):
                w15 = w[i-15]
                w2 = w[i-2]
                s0 = self.rotate_right(w15, 7) ^ self.rotate_right(w15, 18) ^ (w15 >> 3)
                s1 = self.rotate_right(w2, 17) ^ self.rotate_right(w2, 19) ^ (w2 >> 10)
                w.append(int32(w[i-16] + s0 + w[i-7] + s1))
            
            # Compression loop
            for i in range(64):
                a, b, c, d, e, f, g, h_val = current_h
                s1 = self.rotate_right(e, 6) ^ self.rotate_right(e, 11) ^ self.rotate_right(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = int32(h_val + s1 + ch + self.k[i] + w[i])
                
                s0 = self.rotate_right(a, 2) ^ self.rotate_right(a, 13) ^ self.rotate_right(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = int32(s0 + maj)
                
                current_h = [int32(temp1 + temp2), a, b, c, int32(d + temp1), e, f, g]

            for i in range(8):
                current_h[i] = int32(current_h[i] + old_h[i])
        
        # Update persistent state for the next call (the "bug")
        self.h = current_h[:]
        
        # Convert hash to hex string
        res = ""
        for val in current_h[:8]:
            res += f"{val:08x}"
        return res

# 3. Main Solving Logic
def solve():
    # Generate the secret: sha256("0") + sha256("1") [Chained]
    sha = CustomSHA256()
    h0 = sha.hash("0")
    h1 = sha.hash("1")
    secret = h0 + h1

    # Generate the XOR key 'c'
    rng = mulberry32(0)
    c_hex_str = ""
    for _ in range(128):
        idx = int(rng() * 64 + 39)
        c_hex_str += secret[idx]

    # Convert hex string to bytes (parseHexString)
    key_bytes = []
    for i in range(0, len(c_hex_str), 2):
        key_bytes.append(int(c_hex_str[i:i+2], 16))

    # Decode the target flag
    target_b64 = "qncQqyiCZOqEPr2SaRuykxu29zrC17W/8B/KoepEdeZC+KHYV2R/40WM8QA="
    encrypted_bytes = base64.b64decode(target_b64)

    # XOR Decrypt
    flag = "".join(chr(encrypted_bytes[i] ^ key_bytes[i]) for i in range(len(encrypted_bytes)))
    print(f"Decoded Flag: {flag}")

if __name__ == "__main__":
    solve()