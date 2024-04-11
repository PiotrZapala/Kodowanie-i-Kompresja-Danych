import sys
import random
import matplotlib.pyplot as plt

def flip_bit_with_probability(bit, probability):
    if random.random() < probability:
        return 1 - bit
    else:
        return bit

def noise(input_file_path, output_file_path, probability):
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

def compare_files(file0_path, file1_path):
    with open(file0_path, 'rb') as file0, open(file1_path, 'rb') as file1:
        buf0 = file0.read()
        buf1 = file1.read()
        errors = 0

        for i in range(len(buf0)):
            byte0 = buf0[i]
            byte1 = buf1[i]

            segment0 = byte0 >> 4
            segment1 = byte1 >> 4

            if segment0 != segment1:
                errors += 1

            segment0 = byte0 << 4
            segment1 = byte1 << 4

            if segment0 != segment1:
                errors += 1

        return errors

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    probabilities = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    error_rates = []

    for probability in probabilities:
        noise(input_file_path, output_file_path, probability)
        errors = compare_files(input_file_path, output_file_path)
        error_rate = errors / (2*len(open(input_file_path, 'rb').read()))
        error_rates.append(error_rate)

    plt.plot(probabilities, error_rates, marker='o')
    plt.xlabel('Probability')
    plt.ylabel('Error Rate')
    plt.title('Error Rate vs. Probability')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
