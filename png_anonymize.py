import struct


def anonymize_png(input_file, output_file):
    # chunki ktore chcemy zachowac, tylko header i chunk z danymi (end jest zawsze), reszta pomijana
    critical_chunks = {b'IHDR', b'IDAT', b'IEND'}

    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            # przepisuje signature do pliku wyjsciowego
            signature = f_in.read(8)
            f_out.write(signature)

            while True:
                chunk = f_in.read(4)
                if not chunk:
                    break
                chunk_length = struct.unpack('>I', chunk)[0]
                chunk_type = f_in.read(4)
                chunk_data = f_in.read(chunk_length)
                chunk_crc = f_in.read(4)

                if chunk_type[:4] in critical_chunks:
                    # zapisuje dane o critical chunkach do pliku wyjsciowego
                    f_out.write(chunk)
                    f_out.write(chunk_type)
                    f_out.write(chunk_data)
                    f_out.write(chunk_crc)

