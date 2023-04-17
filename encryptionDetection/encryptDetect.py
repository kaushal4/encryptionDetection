import math

class EncryptionDetectionInterface :
    @staticmethod
    def DetectFromByteArray(byte_array:list[bytes]) -> bool :
        # custom implementation of override method
        pass


class EncryptionDetectionShanonEntropy(EncryptionDetectionInterface):
    @staticmethod
    def __GetFreqCount(byte_array: list[bytes]) -> list[int] :
        byte_count = [byte_array.count(bytes([i])) for i in range(0,256)]
        return byte_count

    @staticmethod
    def __GetShannonEntropy(byte_array: list[bytes]):
        entropy = 0.0
        byte_count = EncryptionDetectionShanonEntropy.__GetFreqCount(byte_array)
        for count in byte_count:
            if count == 0:
                continue
            probability = 1.0 * count / len(byte_array)
            entropy -= probability * math.log(probability, 256)
        return entropy

    @staticmethod
    def DetectFromByteArray(byte_array: list[bytes]) -> bool:
        return EncryptionDetectionShanonEntropy.__GetShannonEntropy(byte_array) > 0.65


class EncryptionDetectionFactory :
    @staticmethod
    def getEncryptionAlgorithm(algoritm:str) -> EncryptionDetectionInterface:
        if(algoritm.upper() == "SHANNON"):
            return EncryptionDetectionShanonEntropy()