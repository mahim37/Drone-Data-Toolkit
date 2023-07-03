from src import parse_field_wrecord


def parse_record_osd(ptr, data):
    longitude = parse_field_wrecord.note_8byte_field_radians("OSD.longitude", ptr, data)
    latitude = parse_field_wrecord.note_8byte_field_radians("OSD.latitude", ptr, data)
    height = parse_field_wrecord.note_2byte_field_signed("OSD.height", ptr, data, 10)
