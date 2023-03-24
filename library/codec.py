import abc


class Codec(abc.ABC):
    @abc.abstractmethod
    def encode(self, number: str) -> str:
        pass

    @abc.abstractmethod
    def decode(self, number: str) -> str:
        pass


@Codec.register
class BinaryCodec(Codec):
    def encode(self, binary):
        return binary

    def decode(self, binary):
        return binary


@Codec.register
class GrayCodec(Codec):
    def encode(self, binary):
        grey = binary[0]
        for i in range(1, len(binary)):
            grey += str(int(binary[i - 1]) ^ int(binary[i]))
        return grey

    def decode(self, gray):
        binary = gray[0]
        for i in range(1, len(gray)):
            binary += str(int(binary[i - 1]) ^ int(gray[i]))
        return binary
