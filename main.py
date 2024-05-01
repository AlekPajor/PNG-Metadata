from png_info import get_png_info

file_path = "donek2.png"
try:
    png_info = get_png_info(file_path)
    for key, value in png_info.items():
        if key == "Palette" and value is not None:
            print("Palette:")
            for i, (r, g, b) in enumerate(value):
                print(f"  Color {i + 1}: R: {r}, G: {g}, B: {b}")
        elif key == "sRGB Rendering Intent":
            print("sRGB Rendering Intent:")
            if value is not None:
                print(f"  Rendering Intent: {value}")
            else:
                print("  Not available")
        elif key == "IDAT Size":
            print(f"{key}: {value} bytes")
        elif key == "Chromaticities":
            print("Chromaticities:")
            if value is not None:
                print(f"  White Point: ({value[0]}, {value[1]})")
                print(f"  Red: ({value[2]}, {value[3]})")
                print(f"  Green: ({value[4]}, {value[5]})")
                print(f"  Blue: ({value[6]}, {value[7]})")
            else:
                print("  Not available")
        elif key == "Physical Dimensions":
            print("Physical Dimensions:")
            if value is not None:
                pixels_per_unit, pixels_per_unit_y, unit = value
                print(f"  Pixels Per Unit X: {pixels_per_unit}")
                print(f"  Pixels Per Unit Y: {pixels_per_unit_y}")
                print(f"  Unit: {'Meters' if unit == 1 else 'Unknown'}")
            else:
                print("  Not available")
        elif key == "iTXt Data":
            print("iTXt Data:")
            if value:
                for keyword, text in value.items():
                    print(f"  Keyword: {keyword}, Text: {text}")
            else:
                print("  Not available")
        elif key != "Palette" and key != "IDAT Size" and key != "sRGB Rendering Intent" and key != "Chromaticities" and key != "ICCP Data" and key != "Physical Dimensions":
            print(f"{key}: {value}")
except ValueError as e:
    print(e)

# cHRM: donek
# sRGB: gombek, stereoscopic
# bKGD: donek2
# iTXT: exif
# PLTE: stereoscopic, view
