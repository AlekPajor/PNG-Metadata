from png_info import get_png_info
from png_anonymize import anonymize_png

# ============ READ PNG METADATA ============

# cHRM: donek
# sRGB: gombek, stereoscopic
# bKGD: donek2
# iTXT: exif
# PLTE: stereoscopic, view

file_path = "shrek.png"
try:
    png_info = get_png_info(file_path)
    for key, value in png_info.items():
        if key == "Palette":
            print(f"{key}:")
            if value is not None:
                for i, (r, g, b) in enumerate(value):
                    print(f"  Color {i + 1}: R:{r}, G:{g}, B:{b}")
            else:
                print("  Not available")
        elif key == "Background Color":
            print(f"{key}:")
            if value is not None:
                print(f"{value}")
            else:
                print("  Not available")
        elif key == "sRGB Rendering Intent":
            print(f"{key}:")
            if value is not None:
                print(f"  Rendering Intent: {value}")
            else:
                print("  Not available")
        elif key == "IDAT Size":
            print(f"{key}:")
            if value is not None:
                print(f"  {value} bytes")
            else:
                print("  Not available")
        elif key == "Chromaticities":
            print(f"{key}:")
            if value is not None:
                print(f"  White Point: ({value[0]}, {value[1]})")
                print(f"  Red: ({value[2]}, {value[3]})")
                print(f"  Green: ({value[4]}, {value[5]})")
                print(f"  Blue: ({value[6]}, {value[7]})")
            else:
                print("  Not available")
        elif key == "Physical Dimensions":
            print(f"{key}:")
            if value is not None:
                pixels_per_unit_x, pixels_per_unit_y, unit = value
                print(f"  Pixels Per Unit X: {pixels_per_unit_x}")
                print(f"  Pixels Per Unit Y: {pixels_per_unit_y}")
                print(f"  Unit: {'Meters' if unit == 1 else 'Unknown'}")
            else:
                print("  Not available")
        elif key == "iTXt Data":
            print(f"{key}:")
            if value:
                for keyword, text in value.items():
                    print(f"  Keyword: {keyword}")
                    print(f"  Text: {text}")
            else:
                print("  Not available")
        else:
            print(f"{key}: {value}")
except ValueError as e:
    print(e)


# ============ ANONYMIZE FILE ============

input_filename = "donek2.png"
anonymized_filename = "anonymized.png"
anonymize_png(input_filename, anonymized_filename)