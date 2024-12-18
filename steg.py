import cv2
import numpy as np

def data2binary(data):
    if type(data) == str:
        return ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, '08b') for i in data]
    return None

def hide_data(image, data, security_code):
    data = security_code + "|" + data + "$$"
    binary_data = data2binary(data)
    data_index = 0
    data_length = len(binary_data)

    for row in image:
        for pixel in row:
            r, g, b = data2binary(pixel)
            if data_index < data_length:
                pixel[0] = int(r[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_length:
                pixel[1] = int(g[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index < data_length:
                pixel[2] = int(b[:-1] + binary_data[data_index], 2)
                data_index += 1
            if data_index >= data_length:
                break
        if data_index >= data_length:
            break
    return image

def extract_data(image, provided_code):
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = data2binary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes = [binary_data[i: i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-2:] == "$$":
            break

    if "$$" not in decoded_data:
        return None, None

    decoded_data = decoded_data[:-2]
    if "|" not in decoded_data:
        return None, None

    security_code, message = decoded_data.split("|", 1)
    if provided_code == security_code:
        return message, security_code
    else:
        return None, None

def encode():
    img_name = input("Enter the name of the image to encode (with extension): ")
    image = cv2.imread(img_name)
    if image is None:
        print("Error: Image not found!")
        return

    data = input("Enter the message to hide: ")
    if len(data) == 0:
        print("Error: Message is empty!")
        return

    security_code = input("Enter a security code for this message: ")
    if len(security_code) == 0:
        print("Error: Security code cannot be empty!")
        return

    encoded_img_name = input("Enter the name for the encoded image (with extension): ")
    encoded_image = hide_data(image, data, security_code)
    cv2.imwrite(encoded_img_name, encoded_image)
    print(f"Message successfully encoded in {encoded_img_name}")

def decode():
    img_name = input("Enter the name of the image to decode (with extension): ")
    image = cv2.imread(img_name)
    if image is None:
        print("Error: Image not found!")
        return

    provided_code = input("Enter the security code: ")
    decoded_message, security_code = extract_data(image, provided_code)
    if decoded_message is None:
        print("No hidden message found in this image or the security code is incorrect.")
    else:
        print(f"Decoded message: {decoded_message}")

def steganography():
    while True:
        print("\nImage Steganography Menu:")
        print("1. Encode (Hide a message)")
        print("2. Decode (Extract a message)")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            encode()
        elif choice == 2:
            decode()
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

steganography()
