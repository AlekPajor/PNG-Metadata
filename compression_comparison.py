from PIL import Image
import zlib
import os


def compress_to_png(input_image_path, output_png_path):
    image = Image.open(input_image_path)
    image.save(output_png_path, format='PNG')


def compress_to_zip(input_image_path, output_zip_path):
    with open(input_image_path, 'rb') as f:
        image_data = f.read()
    compressed_data = zlib.compress(image_data)
    with open(output_zip_path, 'wb') as f:
        f.write(compressed_data)


def get_file_size(file_path):
    return os.path.getsize(file_path)


def calculate_compression_ratio(original_size, compressed_size):
    return original_size / compressed_size


# Input image path
input_image_path = 'sunflower.jpg'

# Output paths for compressed files
png_output_path = 'compressed_image_PNG.png'
zip_output_path = 'compressed_image_ZIP.zip'

# Compress image to PNG
compress_to_png(input_image_path, png_output_path)

# Compress image to ZIP
compress_to_zip(input_image_path, zip_output_path)

# Get file sizes
original_size = get_file_size(input_image_path)
png_size = get_file_size(png_output_path)
zip_size = get_file_size(zip_output_path)

# Calculate compression ratios
png_compression_ratio = calculate_compression_ratio(original_size, png_size)
zip_compression_ratio = calculate_compression_ratio(original_size, zip_size)

# Print results
print(f'Original image size: {original_size} bytes')
print(f'PNG compressed image size: {png_size} bytes (Compression ratio: {png_compression_ratio:.2f})')
print(f'ZIP compressed image size: {zip_size} bytes (Compression ratio: {zip_compression_ratio:.2f})')
