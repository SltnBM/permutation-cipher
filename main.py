import math
import random
from typing import List

def validate_key(key: List[int], m: int) -> bool:
    return sorted(key) == list(range(1, m+1))

def pad_plaintext(plaintext: str, m: int, pad_char: str = 'X') -> str:
    n_blocks = math.ceil(len(plaintext) / m)
    total_len = n_blocks * m
    return plaintext.ljust(total_len, pad_char)

def encrypt(plaintext: str, key: List[int], m: int, pad_char: str = 'X') -> str:
    if not validate_key(key, m):
        raise ValueError("Invalid key: must be a permutation of 1..m")

    pt = pad_plaintext(plaintext, m, pad_char)
    ciphertext = []

    for i in range(0, len(pt), m):
        block = pt[i:i+m]
        out_block = [''] * m
        for j in range(m):
            source_pos = key[j] - 1
            out_block[j] = block[source_pos]
        ciphertext.append(''.join(out_block))

    return ''.join(ciphertext)

def decrypt(ciphertext: str, key: List[int], m: int, pad_char: str = 'X') -> str:
    if not validate_key(key, m):
        raise ValueError("Invalid key: must be a permutation of 1..m")

    if len(ciphertext) % m != 0:
        raise ValueError("Ciphertext length must be a multiple of block size")

    plaintext_blocks = []
    for i in range(0, len(ciphertext), m):
        out_block = ciphertext[i:i+m]
        block = [''] * m
        for j in range(m):
            source_pos = key[j] - 1
            block[source_pos] = out_block[j]
        plaintext_blocks.append(''.join(block))

    pt = ''.join(plaintext_blocks)
    return pt.rstrip(pad_char)

def random_key(m: int) -> List[int]:
    arr = list(range(1, m+1))
    random.shuffle(arr)
    return arr

# ----- Interactive version -----
if __name__ == "__main__":
    while True:
        print("=== Permutation Cipher Program ===")
        print("This program encrypts and decrypts text using block transposition.\n")

        choice = input("Choose mode (E = Encrypt, D = Decrypt, B = Both): ").lower().strip()
        text = input("Enter your text: ").replace(" ", "")
        m = int(input("Enter block size (m): "))

        if len(text) % m == 0:
                pad_char = "X"
        else:
            pad_char = input("Enter padding character (default = X): ").strip()
            if not pad_char:
                pad_char = "X"
            else:
                pad_char = pad_char[0]

        while True:
            print("\nEnter your key as space-separated numbers (e.g. '3 1 4 2')")
            print("Or type 'random' to generate a random key")
            key_input = input("Key: ").strip()

            if key_input.lower() == "random":
                key = random_key(m)
                print(f"\nGenerated random key: {key}")
                break
            else:
                try:
                    key = list(map(int, key_input.split()))
                    if validate_key(key, m):
                        break
                    else:
                        print("Invalid key! Must be a permutation of 1..m. Try again.\n")
                except ValueError:
                    print("Invalid input! Please enter numbers only.\n")

        print("\n--- Result ---")
        if choice == "e":
            ciphertext = encrypt(text, key, m, pad_char)
            print("Mode       : Encryption")
            print("Plaintext  :", text)
            print("Key        :", key)
            print("Ciphertext :", ciphertext)
        elif choice == "d":
            plaintext = decrypt(text, key, m, pad_char)
            print("Mode       : Decryption")
            print("Ciphertext :", text)
            print("Key        :", key)
            print("Plaintext  :", plaintext)
        elif choice == "b":
            ciphertext = encrypt(text, key, m, pad_char)
            plaintext = decrypt(ciphertext, key, m, pad_char)
            print("Mode       : Encrypt & Decrypt")
            print("Plaintext  :", text)
            print("Key        :", key)
            print("Ciphertext :", ciphertext)
            print("Decrypted  :", plaintext)
        else:
            print("Invalid choice. Please enter 'E', 'D', or 'B'.")

        again = input("\nTry again? (Y/N): ").lower().strip()
        if again != "y":
            print("Goodbye!")
            break
