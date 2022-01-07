def xor(ba1,ba2):
    """XORing two byte arrays"""
    ba1 = bytearray(ba1)
    ba2 = bytearray(ba2)
    return bytearray([ba1[i] ^ ba2[i] for i in range(len(ba1))])