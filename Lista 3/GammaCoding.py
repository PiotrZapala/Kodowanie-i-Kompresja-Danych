import math

class GammaCoding:

    @staticmethod
    def encode(input_numbers, output_file):
        with open(output_file, 'wb') as output:
            file_content = b''
            padded_zeros_at_the_end = 0
            for num in input_numbers:
                if num == 0:
                    gamma_code = b'10'
                    output.write(gamma_code)
                elif num == 1:
                    gamma_code = b'11'
                    output.write(gamma_code)
                else:
                    num_bits = int(math.log2(num) + 1)
                    gamma_code = b'0' * (num_bits - 1)
                    gamma_code += format(num, '032b')[32 - num_bits:].encode('utf-8')
                    file_content += gamma_code
            for i in range(0, len(file_content), 8):
                chunk = file_content[i:i+8]
                padded_zeros_at_the_end = (8 - len(chunk))
                chunk += b'0' * (8 - len(chunk))
                byte_value = int(chunk, 2)
                output.write(bytes([byte_value]))
            byte_value = padded_zeros_at_the_end.to_bytes(1, byteorder='big')
            output.write(byte_value)


    @staticmethod
    def decode(input_file):
        decoded_numbers = []

        with open(input_file, 'rb') as input_data:
            file_content_bytes = input_data.read()

            file_content = ''.join(format(byte, '08b') for byte in file_content_bytes)
            bits_to_remove = 8 + int(file_content[-8:], 2)
            file_content = file_content[:-bits_to_remove]
            
            if file_content[:2] == '10' and len(file_content) == 2:
                decoded_numbers.append(0)
                return decoded_numbers
            elif file_content[:2] == '11' and len(file_content) == 2:
                decoded_numbers.append(1)
                return decoded_numbers

            index = 0
            while index < len(file_content):
                bit = file_content[index]

                if bit == '0':
                    num_zeros = 1
                    while index < len(file_content) and file_content[index + 1] == '0':
                        num_zeros += 1
                        index += 1

                    binary_representation = ''
                    for _ in range(num_zeros + 1):
                        index += 1
                        binary_representation += file_content[index]

                    num = int(binary_representation, 2)
                    decoded_numbers.append(num)
                elif bit == '1' and file_content[index + 1] == '1':
                    decoded_numbers.append(1)
                    index += 1
                elif bit == '1' and file_content[index + 1] == '0':
                    decoded_numbers.append(0)
                    index += 1

                index += 1

        return decoded_numbers