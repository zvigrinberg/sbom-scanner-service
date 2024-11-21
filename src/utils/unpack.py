import bz2


def unpack_bz2(data: bytes):
    """Unpack bz2 Compressed data into string encoded in UTF-8."""
    return bz2.decompress(data).decode("utf-8")
