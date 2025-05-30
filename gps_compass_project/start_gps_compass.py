#!/usr/bin/env python3
import threading
import time
import rtk_manager
import gps_reader
import subprocess

def main():
    # RTKLIB rtkrcv起動
    rtk_manager.start_rtk_manager()

    # GPS読み取り開始
    gps_reader.start_readers()

    # Flaskサーバー起動
    subprocess.run(["python3", "/home/pi/gps_compass_project/app.py"])

if __name__ == "__main__":
    main()
