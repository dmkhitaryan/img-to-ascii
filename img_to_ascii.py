from PIL import Image
import math
import gui
from pprint import pprint

def rgb_to_brightness(data, transform_type):
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
    return [abs(item - 255) for item in data]
    #return [tuple(map(lambda x: abs(x - 255), item)) for item in data]

def rgb_to_ascii(ascii_chars, data):
    temp = data.copy()
    number_chars = len(ascii_chars)
    interval = math.ceil(255 / len(ascii_chars))
    for index, item in enumerate(temp):
        temp[index] = ascii_chars[ min(math.floor(temp[index] / interval), number_chars - 1) ]
         #print(data[index])
    return temp

def print_ascii_chars(data, img):
    ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    temp = rgb_to_ascii(ascii_chars, data)
    ascii_string = ""
    for i in range(0, len(temp), img.width):
        ascii_string += "".join(temp[i:i+img.width]) + "\n"
    
    return ascii_string.strip()

