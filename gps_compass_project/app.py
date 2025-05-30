from flask import Flask, render_template, jsonify
import folium
from heading_calc import get_latest_positions_and_heading

app = Flask(__name__)

@app.route("/")
def index():
    base_pos, rover_pos, heading_deg, error_m = get_latest_positions_and_heading()
    if base_pos is None or rover_pos is None:
        return "Waiting for GPS data..."

    # folium地図の中心は基準局（base）
    fmap = folium.Map(location=base_pos, zoom_start=18)

    # 基準局マーカー
    folium.Marker(location=base_pos, popup="Base Station", icon=folium.Icon(color="green")).add_to(fmap)

    # 移動局マーカー
    folium.Marker(location=rover_pos, popup=f"Rover<br>Heading: {heading_deg:.1f}°<br>Error: {error_m:.3f} m",
                  icon=folium.Icon(color="red")).add_to(fmap)

    # 方位線（矢印）
    folium.PolyLine(locations=[base_pos, rover_pos], color="blue", weight=3).add_to(fmap)

    # HTMLレンダリング
    map_html = fmap._repr_html_()
    return render_template("map.html", map_html=map_html, heading=heading_deg, error=error_m)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
