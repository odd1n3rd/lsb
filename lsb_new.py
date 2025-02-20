from PIL import Image

def embed_message(input_path, message, output_path):
    img = Image.open(input_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size

    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'

    max_bits = width * height * 3
    if len(binary_message) > max_bits:
        raise ValueError("Message is too long to embed in the image.")

    data = []
    msg_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if msg_index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[msg_index])
                msg_index += 1
            if msg_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[msg_index])
                msg_index += 1
            if msg_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[msg_index])
                msg_index += 1
            data.append((r, g, b))

    stego_img = Image.new('RGB', (width, height))
    stego_img.putdata(data)
    stego_img.save(output_path, 'PNG')

def extract_message(input_path):
    img = Image.open(input_path)
    img = img.convert('RGB')
    pixels = img.getdata()

    binary_message = []
    for pixel in pixels:
        r, g, b = pixel
        binary_message.append(str(r & 1))
        binary_message.append(str(g & 1))
        binary_message.append(str(b & 1))
    binary_message = ''.join(binary_message)

    extracted_bytes = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '00000000':
            break
        extracted_bytes.append(chr(int(byte, 2)))

    return ''.join(extracted_bytes)

def visualize_changes(original_path, stego_path, output_path):
    original_img = Image.open(original_path)
    stego_img = Image.open(stego_path)
    original_img = original_img.convert('RGB')
    stego_img = stego_img.convert('RGB')
    width, height = original_img.size

    vis_img = Image.new('RGB', (width, height), (0, 0, 0))
    vis_pixels = vis_img.load()

    original_pixels = original_img.getdata()
    stego_pixels = stego_img.getdata()
    for i in range(len(original_pixels)):
        original_pixel = original_pixels[i]
        stego_pixel = stego_pixels[i]
        if original_pixel != stego_pixel:
            vis_pixels[i % width, i // width] = (255, 0, 0) 

    vis_img.save(output_path)

embed_message('input.png', 'Secret message', 'stego.png')

message = extract_message('stego.png')
print('Extracted message:', message)

visualize_changes('input.png', 'stego.png', 'visualization.png')