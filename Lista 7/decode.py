import numpy as np
import sys

def hamming_decode(encoded_vector):
    decoded_bits = []
    H = np.array([[1, 0, 1, 1, 1, 0, 0],[1 ,1 ,0 ,1 ,0 ,1 ,0],[1 ,1, 1, 0, 0, 0, 1]])
    
    syndrome = np.dot(H, encoded_vector[:7]) % 2
    
    parity_check = sum(encoded_vector[:7]) % 2 == encoded_vector[7]
    
    if syndrome.any() and parity_check:
        error_index = int(''.join(map(str, syndrome)), 2) - 1
        encoded_vector[error_index] ^= 1
    elif syndrome.any() and not parity_check:
        print("Double error detected")
        return None

    decoded_bits.append(encoded_vector[0])
    decoded_bits.append(encoded_vector[1])
    decoded_bits.append(encoded_vector[2])
    decoded_bits.append(encoded_vector[3])
    return decoded_bits

def main():
    if len(sys.argv) != 3:
        print("Usage: python decode.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    with open(input_file_path, 'rb') as file:
        encoded_data = bytearray(file.read())

    decoded_bits_buffer = []

    for byte in encoded_data:
        encoded_vector = np.array([int(x) for x in np.binary_repr(byte, width=8)], dtype=int)
        decoded_bits = hamming_decode(encoded_vector)
        if decoded_bits is not None:
            decoded_bits_buffer.extend(decoded_bits)

    decoded_bytes = bytearray(int(''.join(map(str, decoded_bits_buffer[i:i+8])), 2) for i in range(0, len(decoded_bits_buffer), 8))
    with open(output_file_path, 'wb') as file:
        file.write(decoded_bytes)

if __name__ == "__main__":
    main()