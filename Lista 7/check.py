import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 check.py <file0> <file1>")
        sys.exit(1)

    file0_path = sys.argv[1]
    file1_path = sys.argv[2]

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

        print(f"Found {errors} Errors")

if __name__ == "__main__":
    main()
