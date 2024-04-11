class FibonacciCoding:

    @staticmethod
    def nth_fib_number(n):
        #if n < 2:
            #return n
        #return FibonacciCoding.nth_fib_number(n-1) + FibonacciCoding.nth_fib_number(n-2)
        fib_num = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
                   987, 1597, 2584, 4181, 10946, 17711, 28657 , 46368,
                   75025, 121393, 196418, 317811, 514229, 832040, 1346269]
        return fib_num[n-1]
    
    @staticmethod
    def encode(input_numbers, output_file):
        with open(output_file, 'wb') as output:
            file_content = b''
            padded_zeros_at_the_end = 0
            for num in input_numbers:
                n = 2
                f_curr = FibonacciCoding.nth_fib_number(n)
                f_prev = f_curr
                while f_curr <= num:
                    n += 1
                    f_prev = f_curr
                    f_curr = FibonacciCoding.nth_fib_number(n)
                fibonacci_code = 2**((n-1)-2)
                num -= f_prev

                while num > 0:
                    n = 2
                    f_curr = FibonacciCoding.nth_fib_number(n)
                    f_prev = f_curr
                    while f_curr <= num:
                        n += 1
                        f_prev = f_curr
                        f_curr = FibonacciCoding.nth_fib_number(n)
                    fibonacci_code += 2**((n-1)-2)
                    num -= f_prev
                binary_fibonacci_code = bin(fibonacci_code)[2:][::-1] + "1"
                file_content += binary_fibonacci_code.encode('utf-8')

            for i in range(0, len(file_content), 8):
                chunk = file_content[i:i+8]
                padded_zeros_at_the_end = (8 - len(chunk))
                chunk += b'0' * padded_zeros_at_the_end
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

            substrings = [substring + '1' for substring in file_content.split('11') if substring]
            for j in range(len(substrings)):
                decoded_number = 0
                i = 2
                for digit in substrings[j]:
                    if digit == "1":
                        decoded_number += FibonacciCoding.nth_fib_number(i)
                    i += 1
                decoded_numbers.append(decoded_number)


        return decoded_numbers