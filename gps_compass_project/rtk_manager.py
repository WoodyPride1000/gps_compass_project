import subprocess
import threading
import time
import os

RTKRCV_CONF = "/home/pi/gps_compass_project/config/rtkrcv.conf"
RTK_OUTPUT = "/home/pi/gps_compass_project/logs/rtk_output.nmea"

class RTKManager:
    def __init__(self):
        self.proc = None
        self.running = True
        self.fix_status = None

    def start_rtkrcv(self):
        cmd = ["rtkrcv", "-s", "-o", RTKRCV_CONF]
        self.proc = subprocess.Popen(cmd)

    def monitor_rtk_output(self):
        while self.running:
            if not os.path.exists(RTK_OUTPUT):
                time.sleep(1)
                continue
            with open(RTK_OUTPUT, "r") as f:
                lines = f.readlines()[-20:]  # 最新20行だけチェック
                for line in lines:
                    if "$GNGGA" in line or "$GPGGA" in line:
                        parts = line.split(",")
                        if len(parts) > 6:
                            fix = parts[6]
                            self.fix_status = fix
            time.sleep(5)

    def get_fix_status(self):
        return self.fix_status

    def stop(self):
        self.running = False
        if self.proc:
            self.proc.terminate()
            self.proc.wait()

rtk_manager = RTKManager()
def start_rtk_manager():
    rtk_manager.start_rtkrcv()
    monitor_thread = threading.Thread(target=rtk_manager.monitor_rtk_output, daemon=True)
    monitor_thread.start()
