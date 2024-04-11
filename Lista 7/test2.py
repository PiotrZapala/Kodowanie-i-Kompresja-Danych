import sys
import random
import numpy as np
import matplotlib.pyplot as plt

def flip_bit_with_probability(bit, probability):
    if random.random() < probability:
        return 1 - bit
    else:
        return bit

def hamming_encode(data_bits):
    G = np.array([[1, 0, 0, 0, 1, 1, 1], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1, 0]])
    
    encoded_vector = np.dot(data_bits, G) % 2

    parity_bit = sum(encoded_vector) % 2
    encoded_vector = np.append(encoded_vector, parity_bit)
    
    return encoded_vector

def test_probability(input_file_path, output_file_path, probability):
    total_blocks = 0
    error_blocks = 0

    with open(input_file_path, 'rb') as input_file:
        with open(output_file_path, 'wb') as output_file:
            while True:
                byte = input_file.read(1)
                if not byte:
                    break 

                byte_value = int.from_bytes(byte, byteorder='big')

                binary_representation = bin(byte_value)[2:]
                binary_representation_8_bits = binary_representation.zfill(8)
                binary_digits = [int(bit) for bit in binary_representation_8_bits]

                encoded_data = []

                encoded_data.extend(hamming_encode(binary_digits[:4]))
                encoded_data.extend(hamming_encode(binary_digits[4:]))

                encoded_bytes = bytearray(int(''.join(map(str, encoded_data[i:i+8])), 2) for i in range(0, len(encoded_data), 8))

                for encoded_byte in encoded_bytes:
                    flipped_byte_value = 0
                    for i in range(8):
                        bit = (encoded_byte >> i) & 1
                        flipped_bit = flip_bit_with_probability(bit, probability)
                        flipped_byte_value |= (flipped_bit << i)

                    flipped_byte = flipped_byte_value.to_bytes(1, byteorder='big')
                    output_file.write(flipped_byte)
                
                total_blocks += 1

    with open(input_file_path, 'rb') as input_file:
        with open(output_file_path, 'rb') as output_file:
            while True:
                original_byte = input_file.read(1)
                noisy_byte = output_file.read(1)
                if not original_byte or not noisy_byte:
                    break

                error_count = 0
                for i in range(8):
                    original_bit = (original_byte[0] >> i) & 1
                    noisy_bit = (noisy_byte[0] >> i) & 1
                    if original_bit != noisy_bit:
                        error_count += 1
                
                if error_count >= 2:
                    error_blocks += 1

    error_percentage = (error_blocks / total_blocks) * 100
    return error_percentage

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    probabilities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

    error_percentages = []

    for probability in probabilities:
        error_percentage = test_probability(input_file_path, output_file_path, probability)
        error_percentages.append(error_percentage)
        print(f"Probability {probability}: Error Percentage {error_percentage}%")

    plt.plot(probabilities, error_percentages, marker='o')
    plt.title('Error Percentage vs. Probability')
    plt.xlabel('Probability')
    plt.ylabel('Error Percentage')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
