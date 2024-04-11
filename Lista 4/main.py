import math
from sys import argv

def crop_image(image):
    original_height = len(image)
    original_width = len(image[0])

    cropped_image = [ row[1:original_width-1] for row in image[1:original_height-1]]

    return cropped_image

def read_tga_image(file_path):
    with open(file_path, 'rb') as file:
        print()
        print(file_path[7:])
        print()
        file.seek(12)
        image_width = int.from_bytes(file.read(2), byteorder='little')
        print("image width =",image_width)
        image_height = int.from_bytes(file.read(2), byteorder='little')
        print("image height =",image_height)
        print()
        file.seek(2,1)

        image_pixels = [[(0, 0, 0) for _ in range(image_width+2)] for _ in range(image_height+2)]

        for x in range(image_height, 0, -1):
            for y in range(1,image_width+1):
                blue = int.from_bytes(file.read(1), byteorder='little')
                green = int.from_bytes(file.read(1), byteorder='little')
                red = int.from_bytes(file.read(1), byteorder='little')
                pixel = (red, green, blue)
                image_pixels[x][y] = pixel
        
    return image_pixels

def predictors(image):
    image_height = len(image)
    image_width = len(image[0])

    def predictor_1(image, image_height, image_width, results):
        '''W'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                west_pixel = image[x][y-1]
                sub_pixel = ((pixel[0]-west_pixel[0])%256, (pixel[1]-west_pixel[1])%256, (pixel[2]-west_pixel[2])%256)
                sub_values[x][y] = sub_pixel
        results["W"] = sub_values

    def predictor_2(image, image_height, image_width, results):
        '''N'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                sub_pixel = ((pixel[0]-north_pixel[0])%256, (pixel[1]-north_pixel[1])%256, (pixel[2]-north_pixel[2])%256)
                sub_values[x][y] = sub_pixel
        results["N"] = sub_values
    
    def predictor_3(image, image_height, image_width, results):
        '''NW'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_west_pixel = image[x-1][y-1]
                sub_pixel = ((pixel[0]-north_west_pixel[0])%256, 
                             (pixel[1]-north_west_pixel[1])%256,
                             (pixel[2]-north_west_pixel[2])%256)
                sub_values[x][y] = sub_pixel
        results["NW"] = sub_values
    
    def predictor_4(image, image_height, image_width, results):
        '''N + W - NW'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                west_pixel = image[x][y-1]
                north_west_pixel = image[x-1][y-1]
                sub_pixel = ((pixel[0]-(north_pixel[0] + west_pixel[0] - north_west_pixel[0]))%256, 
                             (pixel[1]-(north_pixel[1] + west_pixel[1] - north_west_pixel[1]))%256,
                             (pixel[2]-(north_pixel[2] + west_pixel[2] - north_west_pixel[2]))%256)
                sub_values[x][y] = sub_pixel
        results["N + W - NW"] = sub_values

    def predictor_5(image, image_height, image_width, results):
        '''N + (W - NW)/2'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                west_pixel = image[x][y-1]
                north_west_pixel = image[x-1][y-1]
                sub_pixel = ((pixel[0]-(north_pixel[0] + (west_pixel[0] - north_west_pixel[0])/2))%256, 
                             (pixel[1]-(north_pixel[1] + (west_pixel[1] - north_west_pixel[1])/2))%256,
                             (pixel[2]-(north_pixel[2] + (west_pixel[2] - north_west_pixel[2])/2))%256)
                sub_values[x][y] = sub_pixel
        results["N + (W - NW)/2"] = sub_values

    def predictor_6(image, image_height, image_width, results):
        '''W + (N - NW)/2'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                west_pixel = image[x][y-1]
                north_west_pixel = image[x-1][y-1]
                sub_pixel = ((pixel[0]-(west_pixel[0] + (north_pixel[0] - north_west_pixel[0])/2))%256, 
                             (pixel[1]-(west_pixel[1] + (north_pixel[1] - north_west_pixel[1])/2))%256,
                             (pixel[2]-(west_pixel[2] + (north_pixel[2] - north_west_pixel[2])/2))%256)
                sub_values[x][y] = sub_pixel
        results["W + (N - NW)/2"] = sub_values

    def predictor_7(image, image_height, image_width, results):
        '''(N + W)/2'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                west_pixel = image[x][y-1]
                sub_pixel = ((pixel[0]-(west_pixel[0] + north_pixel[0])/2)%256, 
                             (pixel[1]-(west_pixel[1] + north_pixel[1])/2)%256,
                             (pixel[2]-(west_pixel[2] + north_pixel[2])/2)%256)
                sub_values[x][y] = sub_pixel
        results["(N + W)/2"] = sub_values

    def predictor_8(image, image_height, image_width, results):
        '''new standard'''
        sub_values = [[(0, 0, 0) for _ in range(image_width)] for _ in range(image_height)]
        for x in range(1, image_height-1):
            for y in range(1, image_width-1):
                pixel =  image[x][y]
                north_pixel = image[x-1][y]
                west_pixel = image[x][y-1]
                north_west_pixel = image[x-1][y-1]
                rgb = []
                for i in range(0,3):
                    if north_west_pixel[i] >= max(north_pixel[i], west_pixel[i]):
                        rgb.append(max(pixel[i]-north_pixel[i], pixel[i]-west_pixel[i]))
                    elif north_west_pixel[i] <= min(north_pixel[i], west_pixel[i]):
                         rgb.append(min(pixel[i]-north_pixel[i], pixel[i]-west_pixel[i]))
                    else: 
                        rgb.append(pixel[i] - (west_pixel[i] + north_pixel[i] - north_west_pixel[i]))
                sub_values[x][y] = (rgb[0], rgb[1], rgb[2])
        results["new standard"] = sub_values

    results = dict()
    predictor_1(image, image_height, image_width, results)
    predictor_2(image, image_height, image_width, results)
    predictor_3(image, image_height, image_width, results)
    predictor_4(image, image_height, image_width, results)
    predictor_5(image, image_height, image_width, results)
    predictor_6(image, image_height, image_width, results)
    predictor_6(image, image_height, image_width, results)
    predictor_7(image, image_height, image_width, results)
    predictor_8(image, image_height, image_width, results)

    return results

def count_number_of_symbol_occurrences(image):
    pixel_frequency_dictionary = dict()
    red_frequency_dictionary = dict()
    green_frequency_dictionary = dict()
    blue_frequency_dictionary = dict()

    for row in image:
        for pixel in row:
            pixel_frequency_dictionary[pixel] = pixel_frequency_dictionary.get(pixel, 0) + 1

            red_frequency_dictionary[pixel[0]] = red_frequency_dictionary.get(pixel[0], 0) + 1
            green_frequency_dictionary[pixel[1]] = green_frequency_dictionary.get(pixel[1], 0) + 1
            blue_frequency_dictionary[pixel[2]] = blue_frequency_dictionary.get(pixel[2], 0) + 1

    return pixel_frequency_dictionary, red_frequency_dictionary, green_frequency_dictionary, blue_frequency_dictionary

def entropy(image):
    pixel_frequency, red_frequency, green_frequency, blue_frequency = count_number_of_symbol_occurrences(image)

    def calculate_entropy(frequency_dictionary):
        total_symbols = sum(frequency_dictionary.values())
        entropy_value = 0.0

        for frequency in frequency_dictionary.values():
            probability = frequency / total_symbols
            entropy_value -= probability * math.log2(probability)

        return entropy_value

    pixel_entropy = calculate_entropy(pixel_frequency)
    red_entropy = calculate_entropy(red_frequency)
    green_entropy = calculate_entropy(green_frequency)
    blue_entropy = calculate_entropy(blue_frequency)

    return pixel_entropy, red_entropy, green_entropy, blue_entropy
    
def main():
    if len(argv) < 2:
        exit('usage: ./main.py <input file>')

    file_path = argv[1]
    image = read_tga_image(file_path)
    pixels = crop_image(image)
    pixel_entropy, red_entropy, green_entropy, blue_entropy = entropy(pixels)

    print("Original image")
    print("Pixel Entropy:", pixel_entropy)
    print("Red Entropy:", red_entropy)
    print("Green Entropy:", green_entropy)
    print("Blue Entropy:", blue_entropy)
    print()

    results = predictors(image)
    methods = ["W", "N", "NW", "N + W - NW", "N + (W - NW)/2", "W + (N - NW)/2", "(N + W)/2", "new standard"]
    red = dict()
    green = dict()
    blue = dict()
    for method in methods:
        pixel_entropy, red_entropy, green_entropy, blue_entropy = entropy(results[method])
        red[method] = red_entropy
        green[method] = green_entropy
        blue[method] = blue_entropy
        print("Predictor", method)
        print("Pixel Entropy:", pixel_entropy)
        print("Red Entropy:", red_entropy)
        print("Green Entropy:", green_entropy)
        print("Blue Entropy:", blue_entropy)
        print()
    min_red_value = min(red.values())
    min_green_value = min(green.values())
    min_blue_value = min(blue.values())

    min_red_method = [key for key, value in red.items() if value == min_red_value]
    min_green_method = [key for key, value in green.items() if value == min_green_value]
    min_blue_method = [key for key, value in blue.items() if value == min_blue_value]

    print("Best entropy for red channel:", min_red_value, "for predictor:", min_red_method)
    print("Best entropy for green channel:", min_green_value, "for predictor:", min_green_method)
    print("Best entropy for blue channel:", min_blue_value, "for predictor:", min_blue_method)

if __name__ == '__main__':
    main()
