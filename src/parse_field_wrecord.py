import math

from src import unpack


def note_8byte_field_radians(label, ptr, data):
    value = float(unpack.unpack_double_le(ptr, data))
    value = value * 180 / math.pi
    return value


def note_2byte_field_signed(label, ptr, data, divisor=0, offset=0):
    return note_2byte_field(label, ptr, data, divisor, offset, True)


def note_2byte_field(label, ptr, data, divisor=0, offset=0, is_signed=0):
    byte = unpack.unpack_uint16_le(ptr, data)
    byte -= offset
    value = 0
    if divisor != 0:
        if is_signed:
            value = int(byte) / divisor
        else:
            value = byte / divisor
    return value


def note_byte_field(label, ptr, data, divisor=0, is_signed=0):
    byte = unpack.unpack_uint8(ptr, data)
    value = 0
    if divisor != 0:
        if is_signed:
            value = int(byte) / divisor
        else:
            value = byte / divisor
    return value


def sub_byte_field(label, data_byte, mask):
    result = data_byte & mask
    while mask != 0x00 and (mask & 0x01) == 0:
        result = result >> 1
        mask = mask >> 1
    return result


def note_string_field(label, ptr, data, length):
    if ptr[0] > len(data) - length:
        raise ValueError("END_OF_DATA")
    result = ""
    for i in range(length):
        byte = data[ptr[0]]
        result += chr(byte) if byte else ""
        ptr[0] += 1

    return result
