import pandas as pd

from src import parse_field_wrecord, unpack


def parse_record_osd(ptr, data, length):
    column = ['Latitude', 'Longitude', 'Height', 'x_Speed', 'y_Speed', 'z_Speed', 'Pitch',
              'roll', 'yaw', 'rc_State', 'flyc_State', 'flyc_command', 'battery', 'flight_time']
    longitude = parse_field_wrecord.note_8byte_field_radians("OSD.longitude", ptr, data)
    latitude = parse_field_wrecord.note_8byte_field_radians("OSD.latitude", ptr, data)

    length -= 16
    height = parse_field_wrecord.note_2byte_field_signed("OSD.height", ptr, data, 10)
    x_speed = parse_field_wrecord.note_2byte_field_signed("OSD.x_speed", ptr, data, 10)
    y_speed = parse_field_wrecord.note_2byte_field_signed("OSD.y_speed", ptr, data, 10)
    z_speed = parse_field_wrecord.note_2byte_field_signed("OSD.z_speed", ptr, data, 10)
    length -= 8
    pitch = parse_field_wrecord.note_2byte_field_signed("OSD.pitch", ptr, data, 10)
    roll = parse_field_wrecord.note_2byte_field_signed("OSD.roll", ptr, data, 10)
    yaw = parse_field_wrecord.note_2byte_field_signed("OSD.yaw", ptr, data, 10)
    length -= 6

    byte = unpack.unpack_uint8(ptr, data)
    rc_state = parse_field_wrecord.sub_byte_field("OSD.rc_state", byte, 0x80)
    fly_state = parse_field_wrecord.sub_byte_field("OSD.fly_state", byte, 0x7F)
    fly_command = parse_field_wrecord.note_byte_field("OSD.fly_command.RAW", ptr, data)

    byte = unpack.unpack_uint8(ptr, data)
    go_home_status = parse_field_wrecord.sub_byte_field("OSD.go_home_status.RAW", byte, 0xE0)
    is_swave_work = parse_field_wrecord.sub_byte_field("OSD.is_swave_work", byte, 0x10)
    is_motor_up = parse_field_wrecord.sub_byte_field("OSD.is_motor_up", byte, 0x08)
    is_ground_or_sky = parse_field_wrecord.sub_byte_field("OSD.is_ground_or_sky", byte, 0x06)
    can_ioc_work = parse_field_wrecord.sub_byte_field("OSD.can_IOC_work", byte, 0x01)

    byte = unpack.unpack_uint8(ptr, data)
    # Unpack...

    byte = unpack.unpack_uint8(ptr, data)
    # Unpack... Batttery

    byte = unpack.unpack_uint8(ptr, data)
    length -= 5
    # Unpack
    gps_num = parse_field_wrecord.note_byte_field("OSD.gps_num", ptr, data)
    flight_action = parse_field_wrecord.note_byte_field("OSD.flight_action.RAW", ptr, data)
    motor_fail_cause = parse_field_wrecord.note_byte_field("OSD.motor_fail_cause.RAW", ptr, data)

    byte = unpack.unpack_uint8(ptr, data)

    length -= 4

    battery = parse_field_wrecord.note_byte_field("OSD.battery", ptr, data)
    swave_height = parse_field_wrecord.note_byte_field("OSD.sWave_height", ptr, data, 10)
    flight_time = parse_field_wrecord.note_2byte_field_signed("OSD.flight_time", ptr, data, 10)
    motor_revolution = parse_field_wrecord.note_byte_field("OSD.motor_revolutions", ptr, data)

    # Unknown 2 Bytes
    ptr[0] += 2
    length -= 8
    flyc_version = parse_field_wrecord.note_byte_field("OSD.flyc_version", ptr, data)
    drone_type = parse_field_wrecord.note_byte_field("OSD.drone_type.RAW", ptr, data)

    imu_fail_cause = parse_field_wrecord.note_byte_field("OSD.imu_fail_cause", ptr, data)
    length -= 3

    if length > 3:
        motor_fail_reason = parse_field_wrecord.note_byte_field("OSD.motor_fail_reason.RAW", ptr, data)
        # Unknown
        ptr[0] += 1
        ctrl_device = parse_field_wrecord.note_byte_field("OSD.ctrl_device.RAW", ptr, data)
        ptr[0] += 1

    entries = pd.DataFrame([[latitude, longitude, height, x_speed, y_speed, z_speed, pitch, roll, yaw,
                             rc_state, fly_state, fly_command, battery, flight_time]], columns=column)
    entries.to_csv('output.csv', mode='a', index=False)
