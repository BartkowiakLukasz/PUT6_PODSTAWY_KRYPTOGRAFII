import numpy as np
from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_string):
    chars = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

def embed_lsb(image_path, text, output_path):

    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)

    #znacznik konca tekstu
    delimiter = '1111111111111110'
    bin_msg = text_to_binary(text) + delimiter
    
    flat_pixels = pixels.flatten()
    
    if len(bin_msg) > len(flat_pixels):
        raise ValueError("Wiadomość jest za długa dla tego obrazu!")
        
    for i in range(len(bin_msg)):
        #254 = (11111110)
        flat_pixels[i] = (flat_pixels[i] & 254) | int(bin_msg[i])
        
    stego_pixels = flat_pixels.reshape(pixels.shape)
    stego_img = Image.fromarray(stego_pixels.astype(np.uint8))
    stego_img.save(output_path)
    print(f"Zapisano obraz z ukryta wiadomoscia w: {output_path}")

def extract_lsb(image_path):
    img = Image.open(image_path).convert('RGB')
    flat_pixels = np.array(img).flatten()
    
    bin_msg = ''
    delimiter = '1111111111111110'
    
    for p in flat_pixels:
        # Odczyt najmniej znaczącego bitu
        bin_msg += str(p & 1)
        if bin_msg.endswith(delimiter):
            break
            
    if not bin_msg.endswith(delimiter):
        print("Nie znaleziono wiadomosci (brak znacznika konca)!")
        return None
        
    bin_msg = bin_msg[:-len(delimiter)]
    
    return binary_to_text(bin_msg)

def create_difference_map(original_path, stego_path, output_path):
    original = np.array(Image.open(original_path).convert('RGB'), dtype=np.int16)
    stego = np.array(Image.open(stego_path).convert('RGB'), dtype=np.int16)
    
    diff = np.abs(original - stego)
    enhanced_diff = np.where(diff > 0, 255, 0).astype(np.uint8)
    diff_img = Image.fromarray(enhanced_diff)
    diff_img.save(output_path)
    print(f"Mapa różnic została zapisana w: {output_path}")


if __name__ == "__main__":
    print("=== Steganografia LSB ===")
    
    # Generowanie losowego obrazu "nosiciela" do testów (100x100 RGB)
    test_img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    Image.fromarray(test_img).save('lsb_cover.png')
    print("Wygenerowano testowy obraz nosiciela: lsb_cover.png")
    PLIK_WEJSCIOWY = "las.png"
    PLIK_WYJSCIOWY = "las_lsb.png"

    
    secret_message = "To jest tajna wiadomosc wewnatrz obrazka!"
    print(f"Oryginalna wiadomosc: '{secret_message}'")
    
    embed_lsb(PLIK_WEJSCIOWY, secret_message, PLIK_WYJSCIOWY)
    embed_lsb('lsb_cover.png', secret_message, 'lsb_stego.png')
    
    extracted = extract_lsb('lsb_stego.png')
    print(f"Odzyskana wiadomosc: '{extracted}'")

    extracted = extract_lsb(PLIK_WYJSCIOWY)
    print(f"Odzyskana wiadomosc: '{extracted}'")
    
    create_difference_map('lsb_cover.png', 'lsb_stego.png', 'lsb_diff.png')
    create_difference_map(PLIK_WEJSCIOWY, PLIK_WYJSCIOWY, 'las_diff.png')
