import pynmea2
import serial
import threading
import time

BASE_DEVICE = "/dev/ttyUSB0"
ROVER_DEVICE = "/dev/ttyUSB1"

class GPSReader(threading.Thread):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.lat = None
        self.lon = None
        self.lock = threading.Lock()
        self.running = True

    def run(self):
        with serial.Serial(self.device, 4800, timeout=1) as ser:
            while self.running:
                line = ser.readline().decode('ascii', errors='ignore').strip()
                if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
                    try:
                        msg = pynmea2.parse(line)
                        with self.lock:
                            self.lat = msg.latitude
                            self.lon = msg.longitude
                    except pynmea2.ParseError:
                        continue

    def get_position(self):
        with self.lock:
            return (self.lat, self.lon) if self.lat is not None and self.lon is not None else None

    def stop(self):
        self.running = False

base_gps = GPSReader(BASE_DEVICE)
rover_gps = GPSReader(ROVER_DEVICE)

def start_readers():
    base_gps.start()
    rover_gps.start()

def stop_readers():
    base_gps.stop()
    rover_gps.stop()
    base_gps.join()
    rover_gps.join()

def get_positions():
    base_pos = base_gps.get_position()
    rover_pos = rover_gps.get_position()
    return base_pos, rover_pos

if __name__ == "__main__":
    start_readers()
    try:
        while True:
            b, r = get_positions()
            print(f"Base: {b}, Rover: {r}")
            time.sleep(1)
    except KeyboardInterrupt:
        stop_readers()
