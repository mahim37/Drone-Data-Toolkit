from src import parser_osd, unpack, parse_field_wrecord, scramblebytes


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

    def parse_details(self, ptr, data):
        city_part = parse_field_wrecord.note_string_field("DETAILS.city_part", ptr, data, 20)
        street = parse_field_wrecord.note_string_field("DETAILS.street", ptr, data, 20)
        city = parse_field_wrecord.note_string_field("DETAILS.city", ptr, data, 20)
        area = parse_field_wrecord.note_string_field("DETAILS.area", ptr, data, 20)
        is_favorite = parse_field_wrecord.note_byte_field("DETAILS.is_favorite", ptr, data)
        is_new = parse_field_wrecord.note_byte_field("DETAILS.is_new", ptr, data)
        need_upload = parse_field_wrecord.note_byte_field("DETAILS.need_upload", ptr, data)
        # record_line_count = parse_field_wrecord.
        ptr[0] += 4
        # print(city, city_part, area, street)

    def parse_record(self, ptr, data, is_scrambled):
        try:
            record_type = unpack.unpack_uint8(ptr, data)
            record_length = unpack.unpack_uint8(ptr, data)
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
                raise ValueError("Record length exceeds data length")
            if data[ptr[0] + record_length] != 0xFF:
                raise ValueError("Record length does not end with 0xFF")
            record_start = [ptr[0]]
            ptr[0] += record_length + 1
            unscrambled_data = [int for _ in range(record_length - 1)]

            match record_type:
                case 0x01:
                    if is_scrambled:
                        #
                        key_index_low = unpack.unpack_uint8(record_start, data)
                        scramble_table_index = ((record_type - 1) << 8) | key_index_low
                        # print(scramble_table_index) 226
                        record_length -= 1
                        #
                        # if scramble_table_index >= 0x1000:
                        #     raise ValueError("Record length exceeds scramble table")
                        # else:
                        scramble_bytes = scramblebytes.get_scramble_bytes(record_type, key_index_low)
                        # print(scramble_bytes)
                        for i in range(record_length):
                            unscrambled_data[i] = unpack.unpack_uint8(record_start, data) ^ scramble_bytes[i % 8]
                    record_start = [0]
                    parser_osd.parse_record_osd(record_start, bytes(unscrambled_data), record_length)
                case _:
                    pass

                # Implement for other cases.
                # case RECORD_TYPE_HOME:
                #     parse_home.parse_record_home(record_start, bytes(unscrambled_data), record_length)

        except ValueError:
            print("All features were not implemented!!")
            print("Partially Parsed Records.")
            return False

        return True
