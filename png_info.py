import struct
import zlib


def get_png_info(file_path):
    with open(file_path, 'rb') as f:
        # wczytaj signature (8 pierwszych bajtow - czy plik jest w ogole plikiem png)
        signature = f.read(8)
        if signature != b'\x89PNG\r\n\x1a\n':
            # jesli signature sie nie zgadza to znaczy ze nie png
            raise ValueError("File is not a PNG")

        idat_data = b''
        width = height = bit_depth = color_type = compression_method = filter_method = interlace_method = None
        palette = None
        background_color = None
        srgb_rendering_intent = None
        chromaticities = None
        itxt_data = {}   # Dict do danych itxt
        phys_data = None

        while True:
            chunk = f.read(4)
            if not chunk:
                break  # break w iEND robi to samo ale dla pewnosci tutaj tez daje
            chunk_length = struct.unpack('>I', chunk)[0]
            chunk_type = f.read(4)
            chunk_data = f.read(chunk_length)
            chunk_crc = f.read(4)

            if chunk_type == b'IHDR':  # po 4 bajty na wys. i szer. i po bajcie na reszte
                width, height, bit_depth, color_type, compression_method, filter_method, interlace_method = struct.unpack(
                    '>IIBBBBB', chunk_data)
            elif chunk_type == b'PLTE':  # wyciaga po 3 bajty (dla kazdego koloru R, G i B po jednym) i dodaje jako wpis do palety
                palette = [chunk_data[i:i + 3] for i in range(0, len(chunk_data), 3)]
            elif chunk_type == b'IDAT':  # chunk z grafika, ciezko przedstawic tysiace bajtow wiec wyswietlam tylko ich ilosc
                idat_data += chunk_data
            elif chunk_type == b'bKGD':
                if color_type == 3:  # Palette color - pojedynczy bajt do wyciagniecia
                    background_color = struct.unpack('B', chunk_data)[0]
                elif color_type in [0, 4]:  # Grayscale or grayscale with alpha - kolor zapisamy dwubajtowo
                    background_color = struct.unpack('>H', chunk_data)[0]
                elif color_type in [2, 6]:  # Truecolor or truecolor with alpha - wartosci R, G i B, kazda dwubajtowa
                    background_color = struct.unpack('>HHH', chunk_data)[0]
            elif chunk_type == b'sRGB':  # moze nie byc, ale jak jest to bedzie jedna z 4 jednobajtowych wartosci (0-3)
                srgb_rendering_intent = struct.unpack('B', chunk_data)[0]
            elif chunk_type == b'cHRM':  # osmio bajtowy, bo zawiera koordynaty (dwie wartosci [x, y]) czterech chromaticies
                chromaticities = struct.unpack('>IIIIIIII', chunk_data)
            elif chunk_type == b'iTXt':  # wyciagamy wartosci oddzielone binarnymi nullami, ale dla uproszczenia biore tylko keyword i text (zdekodowane do stringow)
                keyword, compression_flag, compression_method, language_tag, translated_keyword, text = chunk_data.split(b'\x00')
                itxt_data[keyword.decode()] = text.decode()
            elif chunk_type == b'pHYs':  # trzy wartosci - ppuX, ppuY, unit (unit jak 1 to metry, a jak 0 to nie ma znaczenia, jednostka abstrakcyjna)
                phys_data = struct.unpack('>IIB', chunk_data)

            elif chunk_type == b'IEND':  # chunk konca pliku
                break  # jak koniec pliku to skoncz wczytywac dalej

        # zdekompresowane dane idat (grafiki), zeby mozna bylo odczytac ich dlugosc
        decompressed_data = zlib.decompress(idat_data)

        return {
            "Width": width,
            "Height": height,
            "Bit Depth": bit_depth,
            "Color Type": color_type,
            "Compression Method": compression_method,
            "Filter Method": filter_method,
            "Interlace Method": interlace_method,
            "IDAT Size": len(decompressed_data),
            "Background Color": background_color,
            "sRGB Rendering Intent": srgb_rendering_intent,
            "Palette": [struct.unpack('BBB', color) for color in palette] if palette else None,
            "Chromaticities": chromaticities,
            "iTXt Data": itxt_data,
            "Physical Dimensions": phys_data
        }
