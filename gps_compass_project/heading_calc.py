import math
from pyproj import Transformer

# WGS84緯度経度 → UTM変換器（日本のZone54Nに設定）
transformer = Transformer.from_crs("epsg:4326", "epsg:32654", always_xy=True)

BASELINE_TRUE = 0.7  # 基線長(m)

def calculate_heading_and_error(base_pos, rover_pos):
    if base_pos is None or rover_pos is None:
        return None, None

    base_x, base_y = transformer.transform(base_pos[1], base_pos[0])  # lon, lat順
    rover_x, rover_y = transformer.transform(rover_pos[1], rover_pos[0])

    dx = rover_x - base_x
    dy = rover_y - base_y

    heading_rad = math.atan2(dx, dy)  # 北を0度とする時計回り
    heading_deg = math.degrees(heading_rad)
    if heading_deg < 0:
        heading_deg += 360

    baseline_measured = math.sqrt(dx*dx + dy*dy)
    error = abs(baseline_measured - BASELINE_TRUE)

    return heading_deg, error

def get_latest_positions_and_heading():
    from gps_reader import get_positions
    base_pos, rover_pos = get_positions()
    heading, error = calculate_heading_and_error(base_pos, rover_pos)
    return base_pos, rover_pos, heading, error
