alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
base = len(alphabet)  


def encode(num: int) -> str:
    if num == 0:
        return alphabet[0]

    chars = []
    while num > 0:
        num, remainder = divmod(num, base)
        chars.append(alphabet[remainder])

    return "".join(reversed(chars))


def decode(short_code: str) -> int:
    num = 0
    for char in short_code:
        num = num * base + alphabet.index(char)
    return num
