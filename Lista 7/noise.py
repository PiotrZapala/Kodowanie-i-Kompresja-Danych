import sys
import random

def flip_bit_with_probability(bit, probability):
    if random.random() < probability:
        return 1 - bit
    else:
        return bit

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 noise.py <input_file> <output_file> <p>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    probability = float(sys.argv[3])

    with open(input_file_path, 'rb') as input_file:
        with open(output_file_path, 'wb') as output_file:
            while True:
                byte = input_file.read(1)
                if not byte:
                    break 

                byte_value = int.from_bytes(byte, byteorder='big')

                flipped_byte_value = 0
                for i in range(8):
                    bit = (byte_value >> i) & 1
                    flipped_bit = flip_bit_with_probability(bit, probability)
                    flipped_byte_value |= (flipped_bit << i)

                flipped_byte = flipped_byte_value.to_bytes(1, byteorder='big')
                output_file.write(flipped_byte)

if __name__ == "__main__":
    main()
