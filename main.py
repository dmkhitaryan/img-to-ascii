from PIL import Image
import math
from pprint import pprint

img = Image.open("./Regulus_Icon.jpg")
#img = img.resize((128,128))
print(f"Successfully loaded image!\nImage size: {img.width} x {img.height}")

def rgb_to_brightness(data, transform_type):
    #print(data)
    match transform_type:
        case "average":
            return [math.floor(sum(item) / 3) for item in data]
        case "luminance":
            return [math.floor(0.2126*item[0] + 0.7152*item[1] + 0.0722*item[2]) for item in data]
        case "desaturation":
            return [math.floor( (max(item) + min(item)) / 2 ) for item in data]
        case "decomposition_min":
            return [math.floor(min(item)) for item in data]
        case "decomposition_max":
            return [math.floor(max(item)) for item in data]
        case _:
            print("Nothing!")
            
def negative_filter(data):
    #print([tuple(map(lambda x: abs(x - 255), item)) for item in data])
    return [tuple(map(lambda x: abs(x - 255), item)) for item in data]

def print_ascii_chars(data):
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    number_chars = len(ascii_chars)
    interval = math.ceil(255 / len(ascii_chars))
    for index, item in enumerate(data):
        data[index] = ascii_chars[ min(math.floor(data[index] / interval), number_chars - 1) ]
         #print(data[index])
     
    for i in range(0, len(data), img.width):
        print(*data[i:i+img.width])
    
                    
data = [img.getpixel((x,y)) for y in range(img.height) for x in range(img.width)]
#data = rgb_to_brightness(data, "average")
#print_ascii_chars(data)
data = negative_filter(data)
data = rgb_to_brightness(data, "average")
print_ascii_chars(data)
