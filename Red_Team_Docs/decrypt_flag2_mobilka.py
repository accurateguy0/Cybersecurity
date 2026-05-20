def decrypt_flag2():
    # The hardcoded check1 value from the Java code
    hex_target = "1a011b075329164d0f012b5004094a471c0c13185326090c06427f1c1f0e4447060800101632"
    
    # Convert hex string to a list of integers
    target_bytes = bytes.fromhex(hex_target)
    
    # The key found in the Logcat
    key = "@string/app_name".encode()
    
    # The Java logic: 
    # str[(length - i) - 1] = str[(length - i) - 1] ^ key[i % key_len]
    # We create a list of the same size to store the result
    result = [0] * len(target_bytes)
    
    for i in range(len(target_bytes)):
        # Calculate the backward index exactly like the Java loop
        idx = (len(target_bytes) - i) - 1
        # XOR the target byte with the key byte
        result[idx] = target_bytes[idx] ^ key[i % len(key)]
        
    return bytes(result).decode()

print(f"Flag 2 Value: {decrypt_flag2()}")