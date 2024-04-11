import math
from collections import Counter

class Entropy:
    
    @staticmethod
    def original_file_entropy(file_path):
        with open(file_path, 'rb') as file:
            bytes_data = file.read()

        chars = Counter(bytes_data)
        total_count = len(bytes_data)

        entropy = 0
        for count in chars.values():
            entropy += count * (-math.log2(count))
        entropy /= total_count
        return entropy + math.log2(total_count)

    @staticmethod
    def encoded_file_entropy(encoded):
        numbers = Counter(encoded)
        total_count = len(encoded)

        entropy = 0
        for count in numbers.values():
            entropy += count * (-math.log2(count))
        entropy /= total_count
        return entropy + math.log2(total_count)