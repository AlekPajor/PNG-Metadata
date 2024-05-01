import struct
import zlib


def get_png_info(file_path):
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        # Read the PNG signature (8 bytes)
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            raise ValueError("File is not a PNG")

        # Initialize variables to store extracted info
        width = height = bit_depth = color_type = compression_method = filter_method = interlace_method = None
        palette = None
        idat_data = b''
        background_color = None
        srgb_rendering_intent = None
        chromaticities = None
        iccp_data = None  # New variable for ICCP chunk
        itxt_data = {}   # Dictionary to store itxt chunk data
        phys_data = None  # New variable for pHYs chunk

        # Loop through chunks
        while True:
            chunk_length_bytes = f.read(4)
            if not chunk_length_bytes:
                break  # No more chunks
            chunk_length = struct.unpack('>I', chunk_length_bytes)[0]
            chunk_type = f.read(4)
            chunk_data = f.read(chunk_length)
            chunk_crc = f.read(4)

            if chunk_type == b'IHDR':  # Image header chunk
                width, height, bit_depth, color_type, compression_method, filter_method, interlace_method = struct.unpack(
                    '>IIBBBBB', chunk_data)
            elif chunk_type == b'PLTE':  # Palette chunk
                palette = [chunk_data[i:i + 3] for i in range(0, len(chunk_data), 3)]
            elif chunk_type == b'IDAT':  # Image data chunk
                idat_data += chunk_data
            elif chunk_type == b'bKGD':  # Background color chunk
                if color_type == 3:  # Palette color
                    background_color = struct.unpack('B', chunk_data)[0]
                elif color_type in [0, 4]:  # Grayscale or grayscale with alpha
                    background_color = struct.unpack('>H', chunk_data)[0]
                elif color_type in [2, 6]:  # Truecolor or truecolor with alpha
                    background_color = struct.unpack('>HHH', chunk_data)
            elif chunk_type == b'sRGB':  # sRGB chunk
                srgb_rendering_intent = struct.unpack('B', chunk_data)[0]
            elif chunk_type == b'cHRM':  # cHRM chunk
                chromaticities = struct.unpack('>IIIIIIII', chunk_data)
            elif chunk_type == b'iTXt':  # iTXt chunk
                keyword, compression_flag, compression_method, language_tag, translated_keyword, text = chunk_data.split(b'\x00')
                itxt_data[keyword.decode()] = text.decode()
            elif chunk_type == b'pHYs':  # pHYs chunk
                phys_data = struct.unpack('>IIB', chunk_data)

            elif chunk_type == b'IEND':  # End chunk
                break  # End of PNG datastream

        # Decompress IDAT data
        decompressed_data = zlib.decompress(idat_data)

        return {
            "Width": width,
            "Height": height,
            "Bit Depth": bit_depth,
            "Color Type": color_type,
            "Compression Method": compression_method,
            "Filter Method": filter_method,
            "Interlace Method": interlace_method,
            "Palette": [struct.unpack('BBB', color) for color in palette] if palette else None,
            "IDAT Size": len(decompressed_data),
            "Background Color": background_color,
            "sRGB Rendering Intent": srgb_rendering_intent,
            "Chromaticities": chromaticities,
            "ICCP Data": iccp_data,  # Include ICCP data in the returned dictionary
            "iTXt Data": itxt_data,  # Include iTXt data in the returned dictionary
            "Physical Dimensions": phys_data  # Include physical dimensions data in the returned dictionary
        }
