import sys
import os
from GammaCoding import GammaCoding
from DeltaCoding import DeltaCoding
from OmegaCoding import OmegaCoding
from FibonacciCoding import FibonacciCoding
from Entropy import Entropy
from Lzw import Lzw

def main():
    if len(sys.argv) < 5:
        print("Usage: python Main.py <--encode|--decode> <--fib|--omega|--gamma|--delta> <input file> <output file>")
        sys.exit(1)

    mode = sys.argv[1]
    coding_type = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]

    if coding_type == "--fib":
        coding = FibonacciCoding()
    elif coding_type == "--delta":
        coding = DeltaCoding()
    elif coding_type == "--gamma":
        coding = GammaCoding()
    elif coding_type == "--omega":
        coding = OmegaCoding()
    if mode == "--encode":
        encoded = Lzw.encode(input_file)
        offset_encoded = [num + 1 for num in encoded]

        coding.encode(offset_encoded, output_file)

        print("Encoded number list entropy:", Entropy.encoded_file_entropy(encoded))
        print("Original file entropy      :", Entropy.original_file_entropy(input_file))

        original_size = os.path.getsize(input_file)
        encoded_size = os.path.getsize(output_file)
        print("Original file size         :", original_size)
        print("Encoded file size          :", encoded_size)
        print("Compression rate           :", original_size / encoded_size)

    elif mode == "--decode":
        decoded_strings = coding.decode(input_file)
        decoded_original_bytes = [num - 1 for num in decoded_strings]
        lzw = Lzw()
        offset_decoded = lzw.decode(decoded_original_bytes)

        with open(output_file, 'wb') as out_file:
            for string in offset_decoded:
                out_file.write(string)

if __name__ == "__main__":
    main()
