import numpy as np
from PIL import Image, ImageDraw

def generate_source_image(width=100, height=100):
    #Tworzy prosty czarno-biały obraz 100x100 do celów testowych.
    # Tryb '1' dla obrazów czarno-białych (1-bitowych)
    image = Image.new('1', (width, height), 1)
    draw = ImageDraw.Draw(image)
    
    draw.rectangle([20, 20, 80, 80], fill=0)
    draw.ellipse([30, 30, 70, 70], fill=1)
    return image

def visual_cryptography_encrypt(image):
    width, height = image.size

    #1 piksel zastępowany jest czterema (kwadrat 2x2).
    out_width = width * 2
    out_height = height * 2
    
    share1 = Image.new('1', (out_width, out_height))
    share2 = Image.new('1', (out_width, out_height))
    
    pixels = image.load()
    s1_pixels = share1.load()
    s2_pixels = share2.load()
    
    # wszystkie mozliwe wzorce z dokladnie 2 czarnymi i 2 bialymi pikselami
    patterns = [
        [(1, 0), (1, 0)],
        [(0, 1), (0, 1)],
        [(1, 1), (0, 0)],
        [(0, 0), (1, 1)],
        [(1, 0), (0, 1)],
        [(0, 1), (1, 0)]
    ]
    
    for y in range(height):
        for x in range(width):
            # Normalizacja wartości piksela do 0 (czarny) lub 1 (biały)
            orig_pixel = 1 if pixels[x, y] > 0 else 0
            
            # Wybór losowego wzorca
            pat_idx = np.random.randint(0, len(patterns))
            pat = patterns[pat_idx]
            
            # Zapisz wzorzec do udziału 1
            s1_pixels[x*2, y*2] = pat[0][0]
            s1_pixels[x*2+1, y*2] = pat[0][1]
            s1_pixels[x*2, y*2+1] = pat[1][0]
            s1_pixels[x*2+1, y*2+1] = pat[1][1]
            
            if orig_pixel == 1: 
                # Piksel biały - udział 2 dostaje taki sam wzorzec
                s2_pixels[x*2, y*2] = pat[0][0]
                s2_pixels[x*2+1, y*2] = pat[0][1]
                s2_pixels[x*2, y*2+1] = pat[1][0]
                s2_pixels[x*2+1, y*2+1] = pat[1][1]
            else: 
                # Piksel czarny - udział 2 dostaje odwrotność wzorca
                s2_pixels[x*2, y*2] = 1 - pat[0][0]
                s2_pixels[x*2+1, y*2] = 1 - pat[0][1]
                s2_pixels[x*2, y*2+1] = 1 - pat[1][0]
                s2_pixels[x*2+1, y*2+1] = 1 - pat[1][1]
                    
    return share1, share2

def combine_shares(share1, share2):
    width, height = share1.size
    combined = Image.new('1', (width, height))
    
    s1_pixels = share1.load()
    s2_pixels = share2.load()
    comb_pixels = combined.load()
    
    for y in range(height):
        for x in range(width):
            p1 = 1 if s1_pixels[x, y] > 0 else 0
            p2 = 1 if s2_pixels[x, y] > 0 else 0
            
            # Nakładanie folii: jeśli jedna jest czarna, to nie przepuszcza światła (wynik = czarny)
            # Konwencja: 0 = czarny, 1 = biały
            if p1 == 0 or p2 == 0:
                comb_pixels[x, y] = 0
            else:
                comb_pixels[x, y] = 1
                
    return combined

if __name__ == "__main__":
    print("Generowanie obrazu zrodlowego 100x100...")
    img = generate_source_image(100, 100)
    img.save("oryginal.png")
    
    print("Szyfrowanie (podzial na 2 udzialy)...")
    s1, s2 = visual_cryptography_encrypt(img)
    s1.save("udzial_1.png")
    s2.save("udzial_2.png")
    
    print("Skladanie udzialow...")
    combined = combine_shares(s1, s2)
    combined.save("zlozone.png")
    
    print("Gotowe! Wygenerowano pliki:")
    print(" - oryginal.png (oryginalny obrazek 100x100)")
    print(" - udzial_1.png (pierwszy udzial 200x200)")
    print(" - udzial_2.png (drugi udzial 200x200)")
    print(" - zlozone.png (zlozenie, z widocznym zaszumieniem, zachowane proporcje)")
