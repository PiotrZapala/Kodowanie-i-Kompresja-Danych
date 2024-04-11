import sys
import random
import numpy as np
import matplotlib.pyplot as plt

double_error_count = 0

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

def hamming_decode(encoded_vector):
    decoded_bits = []
    H = np.array([[1, 0, 1, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1, 0], [1, 1, 1, 0, 0, 0, 1]])
    
    syndrome = np.dot(H, encoded_vector[:7]) % 2
    
    parity_check = sum(encoded_vector[:7]) % 2 == encoded_vector[7]
    
    if syndrome.any() and parity_check:
        error_index = int(''.join(map(str, syndrome)), 2) - 1
        encoded_vector[error_index] ^= 1
    elif syndrome.any() and not parity_check:
        global double_error_count
        double_error_count += 1
        return None

    decoded_bits.append(encoded_vector[0])
    decoded_bits.append(encoded_vector[1])
    decoded_bits.append(encoded_vector[2])
    decoded_bits.append(encoded_vector[3])
    return decoded_bits

def count_double_errors(input_file_path, output_file_path, probability):
    global double_error_count
    double_error_count = 0

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
            
    with open(output_file_path, 'rb') as file:
        encoded_data = bytearray(file.read())
        errors_counter = 0
        for byte in encoded_data:
            encoded_vector = np.array([int(x) for x in np.binary_repr(byte, width=8)], dtype=int)
            decoded_bits = hamming_decode(encoded_vector)
            errors_counter += double_error_count
        double_error_count = 0
    return errors_counter

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    probabilities = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    err = []
    for probability in probabilities:
        double_errors = count_double_errors(input_file_path, output_file_path, probability)
        err.append(double_errors)

    plt.plot(probabilities, err, marker='o')
    plt.title('Double Error Percentage vs. Probability')
    plt.xlabel('Probability')
    plt.ylabel('Double Error Percentage')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
