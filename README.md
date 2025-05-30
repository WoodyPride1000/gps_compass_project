# GPSコンパスプロジェクトの使い方

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourusername/tls-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/tls-analyzer/actions)


## 事前準備

1. 事前準備

1-1. ハードウェア準備
Raspberry Pi 5 (RaspbianなどのLinux環境)
USB GPSモジュール 2台接続
USB0 → 基準局 (Base)
USB1 → 移動局 (Rover)
USB GPSのシリアルデバイスパスは /dev/ttyUSB0, /dev/ttyUSB1 と想定しています。
違う場合は gps_reader.py の BASE_DEVICE, ROVER_DEVICE を修正してください。

1-2. ソフトウェアインストール
ZIPファイルを展開し、Raspberry Pi上の任意のディレクトリ（例：/home/pi/gps_compass_project）に配置してください。
Python3とpipが入っていることを確認。
必要なPythonライブラリをインストール：


cd /home/pi/gps_compass_project
pip3 install -r requirements.txt
RTKLIBの rtkrcv コマンドが使える状態にしてください（sudo apt install rtklib など）。


2. 設定確認

config/rtkrcv.conf の中の設定を確認してください。
シリアルポート名、ボーレート、ログパスなど環境に合わせて調整可能。
基線長（70cm）は baseline-length で設定。
必要に応じて、gps_reader.py のデバイスパスやボーレートも調整してください。


3. 起動方法

3-1. 手動起動
以下のスクリプトを実行して、RTKLIBのrtkrcv起動、GPS読み取り、Flaskサーバー起動を同時に行います。

python3 start_gps_compass.py
Flaskサーバーはデフォルトでポート5000番で起動します。


3-2. Webブラウザで結果確認
Raspberry PiのIPアドレスにブラウザでアクセス：
http://<ラズパイのIPアドレス>:5000/
地図が表示され、基準局（緑マーカー）、移動局（赤マーカー）、方位角、推定誤差がリアルタイムに更新されます。

