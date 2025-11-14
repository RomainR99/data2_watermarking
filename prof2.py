from PIL import Image
import numpy as np

def print_pixel_value(image, x, y):
    value = image[y, x]                                                                                                          
    print("Valeur du pixel :", value)
    print(f"Position x: {x} Position y: {y}")
   

def text_to_binary(text):
    list_of_binary_values = []
    for char in text:
        ascii_value = ord(char)
        binary_ascii_char = bin(ascii_value)[2:]
        binary_ascii_char = binary_ascii_char.zfill(21)
        list_of_binary_values.append(binary_ascii_char)
    binary_text = "".join(list_of_binary_values)
    return binary_text


def get_even_array_image(image):
    even_image = image - image % 2
    return even_image


def watermark_lsb1(even_image, binary_mesage):
    array_of_pixels = even_image.flatten()
    if len(binary_mesage) > len(array_of_pixels):
        raise ValueError("Le message est trop long pour cette image.")
    for index_char in range(len(binary_mesage)):
        bit = binary_mesage[index_char]
        if bit == '1':
            array_of_pixels[index_char] += 1
   
    watermarked_image = array_of_pixels.reshape(even_image.shape)
    print("Message encodé dans l'image.")
    return watermarked_image


def get_message_from_watermarked_image(watermarked_image):
    array_of_pixels = watermarked_image.flatten()
    array_binary_message = array_of_pixels % 2
    list_of_chars = []
    for index in range(0, len(array_binary_message), 21):
        binary_ascii_value = array_binary_message[index: index+21]
        if binary_ascii_value.any():
            char = chr(int("".join([str(value) for value in binary_ascii_value]), 2))
            list_of_chars.append(char)
        else:
             break
        print(binary_ascii_value)
    message = "".join(list_of_chars)
    return message


if __name__ == "__main__":
    image = Image.open("C:/Users/info phone/projets_python/data2_watermarking/OIP .jpg")
    image = image.convert('L')
    print(f"Taille image : {image.size}")
    image.show()
    array_image = np.array(image)

    # print_pixel_value(image, 10, 15)
   
    message_original = "Salut, ça fonctionne !"
    print("Message original :", message_original)
    even_array_image = get_even_array_image(array_image)
    binary_mesage = text_to_binary(message_original)
    watermarked_array_image = watermark_lsb1(even_array_image, binary_mesage)
    Image.fromarray(watermarked_array_image).save("OIP_watermarked.png")
    print("Image encodée sauvegardée.")
    initial_message = get_message_from_watermarked_image(watermarked_array_image)
    print("Message décodé :", initial_message)
    if message_original == initial_message:
        print("\nLes messages sont identiques.")
    else:
        print("\nLes messages sont différents.")
