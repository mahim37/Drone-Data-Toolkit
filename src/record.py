from src import parser_osd, unpack, scramble


class RecordType:
    def __init__(self):
        self.count = 0
        self.min_length = ~0
        self.max_length = 0


class RecordDetail:
    def __init__(self):
        self.num_records = 0
        self.f_max_single_records = 0
        self.record_type_stats = [RecordType() for _ in range(256)]
        self.record_type_names = [str for _ in range(256)]
        self.max_records_for_one_type = 0
        # FieldDataBase

    def parse_record(self, ptr, data, is_scrambled):

        record_type = unpack.unpack_uint8(ptr, data)
        record_length = unpack.unpack_uint8(ptr, data)
        print(record_type, record_length)
        self.num_records += 1
        stat = self.record_type_stats[record_type]
        stat.count += 1
        if stat.count > self.max_records_for_one_type:
            self.max_records_for_one_type = stat.count
        if record_length < stat.min_length:
            stat.min_length = record_length
        if record_length > stat.max_length:
            stat.max_length = record_length

        if ptr[0] + record_length + 1 > len(data):
            raise Exception("Record length exceeds data length")
        if data[ptr[0] + record_length] != 0xFF:
            raise Exception("Record length does not end with 0xFF")
        record_start = [ptr[0]]
        record_limit = [ptr[0] + record_length]
        ptr[0] += record_length + 1
        unscrambled_data = [bytes for _ in range(record_length - 1)]
        print(record_start, record_limit)

        if is_scrambled:
            key_index_low = unpack.unpack_uint8(record_start, data)
            scramble_table_index = ((record_type - 1) << 8) | key_index_low
            record_length -= 1

            if scramble_table_index >= 0x1000:
                raise Exception("Record length exceeds scramble table")
            else:
                scramble_bytes = scramble.scramble_table[scramble_table_index]
                for i in range(record_length):
                    unscrambled_data[i] = unpack.unpack_uint8(record_start, data) ^ scramble_bytes[i % 8]
        record_start = [0]

        match record_type:
            case RECORD_TYPE_OSD:
                parser_osd.parse_record_osd(record_start, bytes(unscrambled_data))
