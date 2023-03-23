import abc


class Codec(abc.ABC):
    @abc.abstractmethod
    def encode(self, to_encode) -> str:
        pass

    @abc.abstractmethod
    def decode(self, to_decode) -> str:
        pass


@Codec.register
class DecimalToBinaryCodec(Codec):
    def encode(self, decimal):
        return bin(decimal)[2:]

    def decode(self, binary):
        return str(int(binary, 2))


@Codec.register
class BinaryToGreyCodec(Codec):
    def encode(self, binary):
        binary = int(binary, 2)
        binary ^= (binary >> 1)
        return bin(binary)[2:]

    def decode(self, gray):
        gray = int(gray, 2)
        mask = gray
        while mask != 0:
            mask >>= 1
            gray ^= mask
        return bin(gray)[2:]
