import numpy as np
from sys import argv

def mse(original, quantized):
    return np.mean((original - quantized) ** 2)

def snr(original, quantized):
    mse_value = mse(original, quantized)
    signal_power = np.mean(original ** 2)
    return 10 * np.log10(signal_power / mse_value)

def getHeaderAndFooter(file):
    header = file.read(18)
    file.seek(-26, 2)
    footer = file.read(26)
    return header, footer

def read_tga_image(file_path):
    with open(file_path, 'rb') as file:
        header, footer = getHeaderAndFooter(file)
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

def quantize_image(image, num_colors, epsilon):
    image_array = np.array(image)
    image_shape = image_array.shape

    flat_image = image_array.reshape((image_shape[0] * image_shape[1], image_shape[2]))

    codebook = initialize_codebook(flat_image, num_colors)
    prev_codebook = np.copy(codebook)

    err = np.inf

    while err > epsilon:
        indices = assign_to_codebook(flat_image, codebook)
        codebook = update_codebook(flat_image, indices, num_colors)
        err = np.sum(np.abs(prev_codebook - codebook))
        prev_codebook = np.copy(codebook)

    quantized_image = codebook[indices].reshape(image_shape)
    return quantized_image.tolist()

def initialize_codebook(data, num_colors):
    indices = np.random.choice(len(data), num_colors, replace=False)
    codebook = data[indices]
    return codebook

def assign_to_codebook(data, codebook):
    distances = np.sum(np.abs(data[:, np.newaxis] - codebook), axis=2)
    indices = np.argmin(distances, axis=1)
    return indices

def update_codebook(data, indices, num_colors):
    codebook = np.zeros((num_colors, data.shape[1]), dtype=np.int64)
    counts = np.zeros(num_colors, dtype=np.uint32)

    for i in range(len(data)):
        index = indices[i]
        codebook[index] += data[i]
        counts[index] += 1

    counts[counts == 0] = 1
    codebook = (codebook / counts[:, np.newaxis]).astype(np.uint8)

    return codebook

def write_tga_image(image, header, footer, output_file):
    image_array = np.array(image, dtype=np.uint8)

    with open(output_file, 'wb') as file:
        file.write(header)

        for row in reversed(image_array):
            for pixel in row:
                blue, green, red = pixel
                file.write(bytes([blue, green, red]))

        file.write(footer)

def main():
    if len(argv) < 2:
        exit('usage: ./main.py <input file> <output file>')

    input_file = argv[1]
    output_file = argv[2]
    num_colors = 16
    epsilon = 0.01

    image, header, footer = read_tga_image(input_file)
    original_image_array = np.array(image, dtype=np.uint8)
    
    quantized_image = quantize_image(image, num_colors, epsilon)
    quantized_image_array = np.array(quantized_image, dtype=np.uint8)

    mse_value = mse(original_image_array, quantized_image_array)
    snr_value = snr(original_image_array, quantized_image_array)

    print(f'Mean Squared Error (MSE): {mse_value}')
    print(f'Signal-to-Noise Ratio (SNR): {snr_value} dB')

    write_tga_image(quantized_image, header, footer, output_file)

if __name__ == '__main__':
    main()
