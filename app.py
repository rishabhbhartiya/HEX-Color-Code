from flask import Flask, render_template, request
from colormath.color_objects import sRGBColor, HSVColor
from colormath.color_conversions import convert_color

app = Flask(__name__)

def get_color_combinations(hex_code):
    base_rgb = sRGBColor.new_from_rgb_hex(hex_code)
    base_hsv = convert_color(base_rgb, HSVColor)

    def to_hex(color):
        return color.get_rgb_hex().upper()

    combinations = {
        "MONOCHROME": [],
        "ANALOGOUS": [],
        "COMPLEMENTARY": [],
        "TRIADIC": [],
        "TETRADIC": []
    }

    # Monochrome Colors
    for brightness in [30, 60, 90, 120]:
        new_color = HSVColor(base_hsv.hsv_h, base_hsv.hsv_s, min(base_hsv.hsv_v * (brightness / 100), 1.0))
        combinations["MONOCHROME"].append(to_hex(convert_color(new_color, sRGBColor)))

    # Analogous Colors
    for angle in [30, -30]:
        new_color = HSVColor((base_hsv.hsv_h + angle) % 360, base_hsv.hsv_s, base_hsv.hsv_v)
        combinations["ANALOGOUS"].append(to_hex(convert_color(new_color, sRGBColor)))

    # Complementary Color
    complementary_color = HSVColor((base_hsv.hsv_h + 180) % 360, base_hsv.hsv_s, base_hsv.hsv_v)
    combinations["COMPLEMENTARY"].append(to_hex(convert_color(complementary_color, sRGBColor)))

    # Triadic Colors
    for angle in [120, -120]:
        new_color = HSVColor((base_hsv.hsv_h + angle) % 360, base_hsv.hsv_s, base_hsv.hsv_v)
        combinations["TRIADIC"].append(to_hex(convert_color(new_color, sRGBColor)))

    # Tetradic Colors
    for angle in [90, 180, 270]:
        new_color = HSVColor((base_hsv.hsv_h + angle) % 360, base_hsv.hsv_s, base_hsv.hsv_v)
        combinations["TETRADIC"].append(to_hex(convert_color(new_color, sRGBColor)))

    return combinations

@app.route("/", methods=["GET", "POST"])
def index():
    base_color = "#264653"  # Default input color
    color_combinations = get_color_combinations(base_color)
    if request.method == "POST" and "color_code" in request.form:
        base_color = request.form["color_code"]
        color_combinations = get_color_combinations(base_color)
    return render_template("index.html", base_color=base_color, color_combinations=color_combinations)

if __name__ == "__main__":
    app.run(debug=True)
