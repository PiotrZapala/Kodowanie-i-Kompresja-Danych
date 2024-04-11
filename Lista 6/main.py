import numpy as np
import sys

def get_header_and_footer(file):
    header = file.read(18)
    file.seek(-26, 2)
    footer = file.read(26)
    return header, footer

def read_tga_image(file_path):
    with open(file_path, 'rb') as file:
        header, footer = get_header_and_footer(file)
        file.seek(12)
        image_width = int.from_bytes(file.read(2), byteorder='little')
        image_height = int.from_bytes(file.read(2), byteorder='little')
        file.seek(2,1)

        image_pixels = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]

        for x in range(image_height - 1, -1, -1):
            for y in range(0, image_width):
                blue = int.from_bytes(file.read(1), byteorder='little')
                green = int.from_bytes(file.read(1), byteorder='little')
                red = int.from_bytes(file.read(1), byteorder='little')
                pixel = (blue, green, red)
                image_pixels[x][y] = pixel

    return image_pixels, header, footer

def write_tga_image(image, header, footer, output_file):
    image_array = np.array(image, dtype=np.uint8)

    with open(output_file, 'wb') as file:
        file.write(header)

        for row in reversed(image_array):
            for pixel in row:
                blue, green, red = pixel
                file.write(bytes([blue, green, red]))

        file.write(footer)

def quantize_difference(difference, k):
    quant_levels = 2 ** k
    max_value = 2 ** (8 - 1)
    quantized_difference = np.floor((difference + max_value) / (256 / quant_levels)) * (256 / quant_levels) - max_value
    return tuple(quantized_difference.astype(int))

def differential_encoding(image_pixels, k):
    encoded_image = []
    reconstructed_previous_pixel = np.array([0, 0, 0], dtype=np.int16)
    for row in image_pixels:
        encoded_row = []
        for pixel in row:
            current_pixel = np.array(pixel, dtype=np.int16)
            diff = current_pixel - reconstructed_previous_pixel
            quantized_diff = quantize_difference(diff, k)
            encoded_row.append(tuple(quantized_diff))
            reconstructed_previous_pixel = reconstructed_previous_pixel + quantized_diff
        encoded_image.append(encoded_row)
    return encoded_image

def differential_decoding(encoded_image):
    decoded_image = []
    reconstructed_previous_pixel = np.array([0, 0, 0], dtype=np.int16)
    for row in encoded_image:
        decoded_row = []
        for quantized_diff in row:
            reconstructed_pixel = reconstructed_previous_pixel + np.array(quantized_diff, dtype=np.int16)
            decoded_row.append(tuple(reconstructed_pixel))
            reconstructed_previous_pixel = reconstructed_pixel
        decoded_image.append(decoded_row)
    return decoded_image

def calculate_mse_snr(original_image, decoded_image):
    original_array = np.array(original_image, dtype=np.float64)
    decoded_array = np.array(decoded_image, dtype=np.float64)
    mse = np.mean((original_array - decoded_array) ** 2)
    snr = 10 * np.log10(np.mean(original_array ** 2) / mse)
    return mse, snr

def calculate_metrics(original_image, decoded_image):
    original_blue = [[pixel[0] for pixel in row] for row in original_image]
    original_green = [[pixel[1] for pixel in row] for row in original_image]
    original_red = [[pixel[2] for pixel in row] for row in original_image]

    decoded_blue = [[pixel[0] for pixel in row] for row in decoded_image]
    decoded_green = [[pixel[1] for pixel in row] for row in decoded_image]
    decoded_red = [[pixel[2] for pixel in row] for row in decoded_image]

    mse_blue, snr_blue = calculate_mse_snr(original_blue, decoded_blue)
    mse_green, snr_green = calculate_mse_snr(original_green, decoded_green)
    mse_red, snr_red = calculate_mse_snr(original_red, decoded_red)

    return {
        'mse': {
            'blue': mse_blue,
            'green': mse_green,
            'red': mse_red
        },
        'snr': {
            'blue': snr_blue,
            'green': snr_green,
            'red': snr_red
        }
    }

def main(operation, input_file_path, output_file_path, k=None):
    original_image, header, footer = read_tga_image(input_file_path)

    if operation == 'encode':
        if k is None:
            raise ValueError("Number of bits (k) must be specified for encoding.")
        encoded_image = differential_encoding(original_image, k)
        write_tga_image(encoded_image, header, footer, output_file_path)

    elif operation == 'decode':
        decoded_image = differential_decoding(original_image)
        write_tga_image(decoded_image, header, footer, output_file_path)

    elif operation == 'metrics':
        decoded_image, header, footer = read_tga_image(output_file_path)
        mse, snr = calculate_mse_snr(original_image, decoded_image)
        print(f"MSE: {mse}, SNR: {snr} dB")

        metrics = calculate_metrics(original_image, decoded_image)
        print(f"MSE (Blue): {metrics['mse']['blue']}, SNR (Blue): {metrics['snr']['blue']} dB")
        print(f"MSE (Green): {metrics['mse']['green']}, SNR (Green): {metrics['snr']['green']} dB")
        print(f"MSE (Red): {metrics['mse']['red']}, SNR (Red): {metrics['snr']['red']} dB")

    else:
        raise ValueError("Operation must be 'encode', 'decode', or 'metrics'.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python main.py <operation> <input_file_path> <output_file_path> [bits]")
        sys.exit(1)

    operation = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    bits = int(sys.argv[4]) if len(sys.argv) > 4 else None

    main(operation, input_file_path, output_file_path, bits)

