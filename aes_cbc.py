import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

import util


class AES_CBC(object):
    def __init__(self, key=get_random_bytes(32)):
        self.key = key
        self._cipher = AES.new(key, AES.MODE_ECB)

    def _add_padding(self, data):
        padding = 16 - (len(data) % 16)
        return data + bytearray([padding for _ in range(padding)])

    def _check_and_strip_padding(self, data):
        data = bytearray(data)
        expected_padding = data[-1]
        if expected_padding == 0 or expected_padding > 16:
            raise ValueError("Incorrect Padding!")
        for byte in data[len(data) - expected_padding:]:
            if byte != expected_padding:
                raise ValueError("Incorrect Padding!")
        return str(data[:len(data) - expected_padding])

    def _split_blocks(self, data):
        length = len(data)
        blocks = []
        for i in range(length / 16):
            blocks.append(data[i * 16:(i + 1) * 16])
        return blocks

    def encrypt(self, plaintext):
        plaintext = self._add_padding(bytearray(plaintext, encoding='utf8'))
        plaintext_blocks = self._split_blocks(plaintext)

        iv = get_random_bytes(16)

        ciphertext_blocks = []
        for i, block in enumerate(plaintext_blocks):
            if i == 0:
                ciphertext_blocks.append(iv)
                ciphertext_blocks.append(self._cipher.encrypt(str(util.xor(iv, block))))
            else:
                ciphertext_blocks.append(self._cipher.encrypt(str(util.xor(ciphertext_blocks[i], block))))

        return base64.b64encode(''.join(ciphertext_blocks))

    def decrypt(self, ciphertext):
        ciphertext = bytearray(base64.b64decode(ciphertext))
        ciphertext_blocks = self._split_blocks(ciphertext)

        plaintext_blocks = []
        for i, block in enumerate(ciphertext_blocks):
            if i == 0:
                continue
            plaintext_blocks.append(str(util.xor(self._cipher.decrypt(str(block)), ciphertext_blocks[i - 1])))
        return self._check_and_strip_padding(''.join(plaintext_blocks))
