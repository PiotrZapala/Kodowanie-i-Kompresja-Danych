import sys
import math

def calculate_frequencies(data):
    symbol_counts = {}
    conditional_counts = {}
    previous_symbol = 0

    for symbol in data:
        if symbol in symbol_counts:
            symbol_counts[symbol] += 1
        else:
            symbol_counts[symbol] = 1

        if previous_symbol not in conditional_counts:
            conditional_counts[previous_symbol] = {}
        if symbol in conditional_counts[previous_symbol]:
            conditional_counts[previous_symbol][symbol] += 1
        else:
            conditional_counts[previous_symbol][symbol] = 1
        previous_symbol = symbol

    return symbol_counts, conditional_counts

def calculate_entropy(symbol_counts):
    total_symbols = sum(symbol_counts.values())
    entropy = 0
    for count in symbol_counts.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_conditional_entropy(symbol_counts, conditional_counts):
    total_symbols = sum(symbol_counts.values())
    conditional_entropy = 0
    for previous_symbol, counts in conditional_counts.items():
        for symbol, count in counts.items():
            p_previous = symbol_counts.get(previous_symbol, 0) / total_symbols
            p_symbol_given_previous = count / symbol_counts.get(previous_symbol, 1)
            conditional_entropy -= p_previous * p_symbol_given_previous * math.log2(p_symbol_given_previous)
    return conditional_entropy

def file_reader(file_name):

    with open(file_name, 'rb') as file:
        data = file.read()
        return data

def main():
    args = sys.argv
    if len(args) > 1:
        file_name = args[1]
        data = file_reader(file_name)
    else: 
        print("Wrong number of arguments!")
        exit(0)

    symbol_counts, conditional_counts = calculate_frequencies(data)
    entropy = calculate_entropy(symbol_counts)
    conditional_entropy = calculate_conditional_entropy(symbol_counts, conditional_counts)
    print(f'Entropia: {entropy}')
    print(f'Entropia warunkowa: {conditional_entropy}')

if __name__ == "__main__":
    main()