import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Dane z zadania
p = 10332921861938291919377635159012636040519117927041835671194203494937679183911345052843111512544303969800681115505917911462916407940308340306260755239268943
A = 8370337962458643162004582468469045984889816058567658904788530882468973454873284491037710219222503893094363658486261941098330951794393018216763327572120119
B = 9755909033513767641159594933585734179714892615169429957597029280980531443144704341694474385957669949989090202320232433789032328934018623049865998847328154
encrypted_flag = "PLCPttoNuN/dZyOWEQVpcu+ZPeKldvA+DqpBQgen9/loHpLKAzUQwL1NqD7TWO0ceGiOXVMk5z5KF1PGhdPUFg=="

# 1. Zakładamy błąd w implementacji: S = A ^ B ^ g
# Najczęstsze g to 2
g = 11
shared_secret = A ^ B ^ g

# 2. Przygotowanie klucza AES (SHA256 z S jako stringa)
key = hashlib.sha256(str(shared_secret).encode()).digest()

# 3. Deszyfrowanie
raw_data = base64.b64decode(encrypted_flag)
iv = raw_data[:16]
ciphertext = raw_data[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
try:
    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print(f"Znaleziona flaga: {decrypted.decode()}")
except Exception as e:
    print("Błąd deszyfrowania. Spróbuj zmienić wartość g (np. na 5) lub formatowanie klucza.")