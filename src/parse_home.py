from src import parse_field_wrecord


def parse_record_home(ptr, data, length):
    longitude = parse_field_wrecord.note_8byte_field_radians("HOME.longitude", ptr, data)
    latitude = parse_field_wrecord.note_8byte_field_radians("HOME.latitude", ptr, data)
