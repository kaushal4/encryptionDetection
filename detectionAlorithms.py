import math


def GetFreqCount(byte_array: list[bytes]) -> list[int]:
    byte_count = [byte_array.count(bytes([i])) for i in range(0, 256)]
    return byte_count


def shannonEntropy(byteArray: list[bytes]):
    entropy = 0.0
    byte_count = GetFreqCount(byteArray)
    for count in byte_count:
        if count == 0:
            continue
        probability = 1.0 * count / len(byteArray)
        entropy -= probability * math.log(probability, 256)
    return entropy


def isEncrypted(byteArray: list[bytes]) -> bool:
    return shannonEntropy(byteArray) > 0.65
