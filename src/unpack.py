import struct


def unpack_uint8(ptr, data):
    if ptr[0] + 1 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('B', data[ptr[0]:ptr[0] + 1])[0]
    ptr[0] += 1
    return result


def unpack_uint16_le(ptr, data):
    if ptr[0] + 2 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('<L', data[ptr[0]:ptr[0] + 2])[0]
    ptr[0] += 2
    return result


def unpack_uint16_be(ptr, data):
    if ptr[0] + 2 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('>L', data[ptr[0]:ptr[0] + 2])[0]
    ptr[0] += 2
    return result


def unpack_uint32_le(ptr, data):
    if ptr[0] + 4 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('<L', data[ptr[0]:ptr[0] + 4])[0]
    ptr[0] += 4
    return result


def unpack_uint32_be(ptr, data):
    if ptr[0] + 4 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('>L', data[ptr[0]:ptr[0] + 4])[0]
    ptr[0] += 4
    return result


def unpack_uint64_le(ptr, data):
    if ptr[0] + 8 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('<Q', data[ptr[0]:ptr[0] + 8])[0]
    ptr[0] += 8
    return result


def unpack_double_le(ptr, data):
    if ptr[0] + 8 > len(data):
        raise ValueError("END_OF_DATA")
    result = struct.unpack('<d', data[ptr[0]:ptr[0] + 8])[0]
    ptr[0] += 8
    return result
