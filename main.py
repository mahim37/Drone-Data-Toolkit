import mmap
import os
import sys

from src import record, unpack

OLD_HEADER_SIZE = 12
NEW_HEADER_SIZE = 100
MIN_RECORD_SIZE = 3


def map_file(path):
    try:
        with open(path, 'rb') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmap_file:
                return mmap_file.read()

    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


def get_file_size(path):
    try:
        size = os.path.getsize(path)
        if size < OLD_HEADER_SIZE:
            print(f"Error: '{path}': Bad File Size: {size} ")
            sys.exit(1)
        else:
            return size
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'.")
    except Exception as e:
        print(f"An error occurred while getting file size: {e}")


if __name__ == '__main__':
    # file_path = input("Enter the path of the text file: ")
    file_path = "SampleData/DJI3.txt"
    file_size = get_file_size(file_path)
    mapped_file = map_file(file_path)
    file_ptr = [0]

    header_record_size = unpack.unpack_uint64_le(file_ptr, mapped_file)
    print("HeaderAndRecord Size: ", header_record_size)

    file_version = unpack.unpack_uint32_be(file_ptr, mapped_file)
    print("File Version: ", hex(file_version))

    is_scrambled = 1 if file_version & 0x0000FF00 >= 0x00000600 else 0
    header_size = NEW_HEADER_SIZE if is_scrambled else OLD_HEADER_SIZE
    min_file_size = header_size + MIN_RECORD_SIZE

    if header_record_size < min_file_size or header_record_size > file_size:
        print(f"Error: '{file_path}': Bad File Size: {header_record_size} ")
        sys.exit(1)

    obj = record.RecordDetail()
    file_ptr[0] = header_record_size
    obj.parse_details(file_ptr, mapped_file)

    file_ptr[0] = header_size
    while file_ptr[0] < len(mapped_file):
        if not obj.parse_record(file_ptr, mapped_file, is_scrambled):
            break
