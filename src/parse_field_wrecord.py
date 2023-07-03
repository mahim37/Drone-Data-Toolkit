import math

from src import unpack


def note_8byte_field_radians(label, ptr, data):
    value = float(unpack.unpack_double_le(ptr, data))
    value = value * 180 / math.pi
    print(label, value)
    return value
