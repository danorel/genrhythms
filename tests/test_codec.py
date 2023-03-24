import pytest

from library.codec import BinaryCodec, GrayCodec


binary_codec = BinaryCodec()
gray_codec = GrayCodec()


@pytest.mark.parametrize("binary,gray", [
    ("1111101111", "1000011000"),
    ("1111101110", "1000011001"),
    ("1010101010", "1111111111"),
    ("0000000000", "0000000000")
])
def test_GrayCodec_encode(binary, gray):
    assert gray_codec.encode(binary) == gray


@pytest.mark.parametrize("gray,binary", [
    ("1000011000", "1111101111"),
    ("1000011001", "1111101110"),
    ("1111111111", "1010101010"),
    ("0000000000", "0000000000")
])
def test_GrayCodec_decode(gray, binary):
    assert gray_codec.decode(gray) == binary
