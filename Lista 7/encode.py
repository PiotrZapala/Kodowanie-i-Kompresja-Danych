import numpy as np
import sys

def hamming_encode(data_bits):
    G = np.array([[1, 0, 0, 0, 1, 1, 1],[0, 1, 0, 0, 0, 1, 1],[ 0, 0 ,1 ,0 ,1 ,0 ,1],[0, 0, 0, 1, 1, 1, 0]])
    
    encoded_vector = np.dot(data_bits, G)%2

    parity_bit = sum(encoded_vector) % 2
    encoded_vector = np.append(encoded_vector, parity_bit)
    
    return encoded_vector

def main():
    if len(sys.argv) != 3:
        print("Usage: python encode.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    with open(input_file_path, 'rb') as file:
        data = file.read()

    encoded_data = []

    for byte in data:
        binary_representation = bin(byte)[2:]
        binary_representation_8_bits = binary_representation.zfill(8)
        binary_digits = [int(bit) for bit in binary_representation_8_bits]

        encoded_data.extend(hamming_encode(binary_digits[:4]))
        encoded_data.extend(hamming_encode(binary_digits[4:]))

    encoded_bytes = bytearray(int(''.join(map(str, encoded_data[i:i+8])), 2) for i in range(0, len(encoded_data), 8))

    with open(output_file_path, 'wb') as file:
        file.write(encoded_bytes)

if __name__ == "__main__":
    main()