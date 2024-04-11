#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <cmath>
#include <stdexcept>

const std::string NYT_CHAR_CODE = "NYT";

class Node {
public:
    Node(Node* parent, int weight = 0, Node* left = nullptr, Node* right = nullptr, const std::string& characters = "")
        : _parent(parent), _weight(weight), _left(left), _right(right), _characters(characters) {}

    Node* parent() const { return _parent; }
    void parent(Node* newParent) { _parent = newParent; }

    int weight() const { return _weight; }
    void weight(int newWeight) { _weight = newWeight; }

    Node* left() const { return _left; }
    void left(Node* newLeft) { _left = newLeft; }

    Node* right() const { return _right; }
    void right(Node* newRight) { _right = newRight; }

    const std::string& characters() const { return _characters; }
    void characters(const std::string& newCharacters) { _characters = newCharacters; }

    bool isLeaf() const {
        return _left == nullptr && _right == nullptr;
    }

private:
    Node* _parent;
    int _weight;
    Node* _left;
    Node* _right;
    std::string _characters;
};

class HuffmanCoding {
public:
    HuffmanCoding()
        : _NYT(new Node(nullptr, 0, nullptr, nullptr, NYT_CHAR_CODE)), _root(_NYT) {
        _allChars.resize(256, nullptr);
    }

    bool isAlreadyAdded(const std::string& characters) const {
        if (characters.length() == 0 || characters.length() > 1 || static_cast<unsigned char>(characters[0]) > 255) {
            throw std::runtime_error("Invalid character");
        }
        return _allChars[static_cast<unsigned char>(characters[0])] != nullptr;
    }

    void registerChar(const std::string& characters) {
        Node* current = _allChars[static_cast<unsigned char>(characters[0])];

        if (current == nullptr) {
            Node* nyt = _NYT;
            Node* oldNytParent = nyt->parent();

            Node* newParent = nullptr;

            if (oldNytParent == nullptr) {
                _root = new Node(nullptr, 0, nyt, nullptr);
                nyt->parent(_root);
                newParent = _root;
            } else {
                newParent = new Node(oldNytParent, 1, nyt, nullptr);
                oldNytParent->left(newParent);
                nyt->parent(newParent);
            }

            Node* newNode = new Node(newParent, 1, nullptr, nullptr, characters);
            newParent->right(newNode);

            _allNodesSorted.push_back(newNode);
            _allNodesSorted.push_back(newParent);

            _allChars[static_cast<unsigned char>(characters[0])] = newNode;

            current = newParent->parent();
        }

        while (current != nullptr) {
            Node* toSwap = nullptr;
            for (Node* n : _allNodesSorted) {
                if (n->weight() == current->weight()) {
                    toSwap = n;
                    break;
                }
            }

            if (current != toSwap && current != toSwap->parent() && toSwap != current->parent()) {
                swapNodes(current, toSwap);
            }

            current->weight(current->weight() + 1);
            current = current->parent();
        }
    }

    std::string getNodeCode(const Node* node) const {
        std::string code = "";
        const Node* currentNode = node;

        while (currentNode->parent() != nullptr) {
            const Node* parent = currentNode->parent();
            if (parent->left() == currentNode) {
                code += '0';
            } else {
                code += '1';
            }
            currentNode = parent;
        }

        return std::string(code.rbegin(), code.rend());
    }

    std::string getCode(const std::string& characters) const {
        if (isAlreadyAdded(characters)) {
            const Node* node = _allChars[static_cast<unsigned char>(characters[0])];
            return getNodeCode(node);
        } else {
            return getNodeCode(_NYT) + std::bitset<8>(characters[0]).to_string();
        }
    }

    std::string encodeSingleCharacter(const std::string& characters) {
        std::string code = getCode(characters);
        registerChar(characters);
        return code;
    }

    std::vector<int> decode(const std::string& encoded) {
        std::vector<int> output;

        char firstChar = static_cast<char>(std::bitset<8>(encoded.substr(0, 8)).to_ulong());
        output.push_back(static_cast<int>(firstChar));

        registerChar(std::string(1, firstChar));

        Node* node = _root;
        size_t i = 8;

        while (i < encoded.size()) {
            char currentBit = encoded[i];

            if (currentBit == '0') {
                node = node->left();
            } else if (currentBit == '1') {
                node = node->right();
            } else {
                throw std::runtime_error("Invalid Huffman code (not a 0 or 1)");
            }


            char decodedChar = node->characters()[0];

            if (decodedChar != '\0') {
                if (node->characters() == NYT_CHAR_CODE) {
                    decodedChar = static_cast<char>(std::bitset<8>(encoded.substr(i + 1, 8)).to_ulong());
                    i += 8;
                }

                output.push_back(static_cast<int>(decodedChar));
                registerChar(std::string(1, decodedChar));
                node = _root;
            }

            i++;
        }

        return output;
    }

    double getAvgCodeLength() const {
        std::vector<size_t> lengths;
        size_t count = 0;

        for (const Node* node : _allChars) {
            if (node != nullptr) {
                lengths.push_back(getNodeCode(node).length());
                count++;
            }
        }

        double sum = 0;
        for (size_t length : lengths) {
            sum += length;
        }

        return sum / count;
    }

    double getEntropy() const {
        double output = 0;

        for (const Node* node : _allChars) {
            if (node != nullptr) {
                output += node->weight() * (-std::log2(node->weight()));
            }
        }

        output /= _root->weight();

        return output + std::log2(_root->weight());
    }

private:
    Node* _NYT;
    Node* _root;
    std::vector<Node*> _allChars;
    std::vector<Node*> _allNodesSorted;

    void swapNodes(Node* one, Node* two) {
        size_t oneIndex = std::distance(_allNodesSorted.begin(), std::find(_allNodesSorted.begin(), _allNodesSorted.end(), one));
        size_t twoIndex = std::distance(_allNodesSorted.begin(), std::find(_allNodesSorted.begin(), _allNodesSorted.end(), two));

        std::swap(_allNodesSorted[oneIndex], _allNodesSorted[twoIndex]);

        Node* parent = one->parent();
        one->parent(two->parent());
        two->parent(parent);

        if (one->parent()->left() == two) {
            one->parent()->left(one);
        } else {
            one->parent()->right(one);
        }

        if (two->parent()->left() == one) {
            two->parent()->left(two);
        } else {
            two->parent()->right(two);
        }
    }
};

int main(int argc, char* argv[]) {
    // Sprawdzenie poprawności liczby argumentów
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <--encode|--decode> <input file> <output file>" << std::endl;
        return 1;
    }

    // Odczyt trybu pracy i nazw plików wejściowego i wyjściowego
    std::string mode = argv[1];
    std::string inputFileName = argv[2];
    std::string outputFileName = argv[3];

    // Inicjalizacja obiektu HuffmanCoding
    HuffmanCoding huffman;

    // Tryb dekodowania
    if (mode == "--decode") {
        // Otwarcie plików do odczytu i zapisu
        std::ifstream inputFile(inputFileName, std::ios::binary);
        std::ofstream outputFile(outputFileName, std::ios::binary);

        // Obsługa błędów przy otwieraniu plików
        if (!inputFile.is_open() || !outputFile.is_open()) {
            std::cerr << "Error opening files" << std::endl;
            return 1;
        }

        // Odczyt ilości użytych bitów na dopełnienie
        std::string inputBits;
        char tmp;
        inputFile.read(&tmp, 1);
        size_t paddingUsed = static_cast<size_t>(tmp);

        // Odczyt bitów z pliku i utworzenie ciągu bitów
        while (inputFile.read(&tmp, 1)) {
            for (int i = 7; i >= 0; --i) {
                inputBits += ((tmp >> i) & 0x01) ? '1' : '0';
            }
        }

        // Usunięcie dopełnienia
        inputBits = inputBits.substr(0, inputBits.length() - paddingUsed);

        // Dekodowanie i zapisanie do pliku wynikowego
        std::vector<int> bytes = huffman.decode(inputBits);
        for (int byte : bytes) {
            outputFile.write(reinterpret_cast<const char*>(&byte), 1);
        }
    } else {  // Tryb kodowania
        // Otwarcie plików do odczytu i zapisu
        std::ifstream inputFile(inputFileName, std::ios::binary);
        std::ofstream outputFile(outputFileName, std::ios::binary);

        // Obsługa błędów przy otwieraniu plików
        if (!inputFile.is_open() || !outputFile.is_open()) {
            std::cerr << "Error opening files" << std::endl;
            return 1;
        }

        // Kodowanie pojedynczych znaków z pliku wejściowego
        std::string output;
        char byte;
        size_t count = 1;
        while (inputFile.read(&byte, 1)) {
            output += huffman.encodeSingleCharacter(std::string(1, byte));
            ++count;
        }

        // Konwersja ciągu bitów na bajty i zapisanie do pliku wynikowego
        std::vector<char> outputBytes;
        size_t paddingUsed = 0;
        for (size_t i = 0; i < std::ceil(output.length() / 8.0); ++i) {
            std::string tmp = output.substr(i * 8, 8);
            if (tmp.length() != 8) {
                paddingUsed = 8 - tmp.length();
                tmp += std::string(paddingUsed, '0');
            }
            outputBytes.push_back(static_cast<char>(std::bitset<8>(tmp).to_ulong()));
        }
        outputBytes.insert(outputBytes.begin(), static_cast<char>(paddingUsed));

        for (char b : outputBytes) {
            outputFile.write(&b, 1);
        }

        // Wyświetlenie statystyk
        std::cout << "Avg codeword length: " << huffman.getAvgCodeLength() << std::endl;
        std::cout << "Compression rate: " << count / static_cast<double>(outputBytes.size()) << std::endl;
        std::cout << "Entropy: " << huffman.getEntropy() << std::endl;
    }

    return 0;
}
