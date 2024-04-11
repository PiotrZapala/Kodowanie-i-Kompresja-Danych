import math

class OmegaCoding:

    @staticmethod
    def encode(input_numbers, output_file):
        with open(output_file, 'wb') as output:
            file_content = b''
            padded_zeros_at_the_end = 0
            for num in input_numbers:
                if num == 0:
                    omega_code = b'10'
                    output.write(omega_code)
                elif num == 1:
                    omega_code = b'11'
                    output.write(omega_code)
                else:
                    omega_code = b'0'

                    while num > 1:
                        binary_representation = bin(num)[2:].encode('utf-8')
                        omega_code = binary_representation + omega_code
                        num = len(binary_representation) - 1
                    file_content += omega_code

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
        with open(input_file, "rb") as input_data:
            file_content_bytes = input_data.read()
            file_content = ''.join(format(byte, '08b') for byte in file_content_bytes)
            bits_to_remove = 8 + int(file_content[-8:], 2)
            file_content = file_content[:-bits_to_remove]
            index = 0
            while index < len(file_content):
                bit = file_content[index]
                n = 1 
                prev_n = n
                while bit != '0':
                    binary_substr = file_content[index:index+n+1]
                    prev_n = n + 1
                    n = int(binary_substr, 2)
                    index = index + prev_n
                    bit = file_content[index]

                decoded_numbers.append(n)
                index += 1

        return decoded_numbers