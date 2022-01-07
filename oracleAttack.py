import base64
from aes_cbc import AES_CBC
import util
from tkinter import *
global_cipher = AES_CBC()


def split_blocks(data):
    length = len(data)
    blocks = []
    for i in range(length / 16):
        blocks.append(data[i * 16:(i + 1) * 16])
    return blocks


def find_bytes(blocks):

    c_prime = bytearray([b for b in blocks[0]])

    plaintext_bytes = bytearray([0 for _ in range(16)])

    for i in range(16):
        expected_padding = bytearray([0 for _ in range(16 - i)] + [(i + 1) for _ in range(i)])
        c_prime = util.xor(util.xor(expected_padding, plaintext_bytes), blocks[0])

        for byte in range(blocks[0][15 - i] + 1, 256) + range(0, blocks[0][15 - i] + 1):

            c_prime[15 - i] = byte
            # c_prime[15] = (plaintext_byte ^ blocks[0][15] ^ 0x02)

            to_test = base64.b64encode(str(c_prime + blocks[1]))

            try:
                global_cipher.decrypt(to_test)
                # global_cipher.decrypt(to_test)
                plaintext_bytes[15 - i] = (byte ^ (i + 1) ^ blocks[0][15 - i])
                break
            except:
                pass
    return ''.join([chr(b) for b in plaintext_bytes if b > 16])


def find_plaintext(ciphertext):
    ciphertext = bytearray(base64.b64decode(ciphertext))
    # ciphertext = bytearray(ciphertext)
    blocks = split_blocks(ciphertext)
    plaintext = ""

    for i in range(len(blocks) - 1):
        plaintext += find_bytes(blocks[i:i + 2])

    return plaintext