import numpy as np
from PIL import Image

def generate_pairs(seed, n_pairs, width, height):
    np.random.seed(seed)
    pairs = []
    for _ in range(n_pairs):
        a = (np.random.randint(0, width), np.random.randint(0, height))
        b = (np.random.randint(0, width), np.random.randint(0, height))
        pairs.append((a, b))
    return pairs

def embed_patchwork(image_path, output_path, seed, n_pairs, d):
    img = Image.open(image_path).convert('YCbCr')
    #y luminacja (jasnosc), cb i cr to chrominacja (kolor)
    y, cb, cr = img.split()
    
    #modyfikujemy jedynie jasnosc pikseli (y)
    pixels_y = np.array(y, dtype=np.int32)
    width, height = img.size
    
    pairs = generate_pairs(seed, n_pairs, width, height)
    
    for a, b in pairs:
        xa, ya = a
        xb, yb = b
        pixels_y[ya, xa] = min(255, pixels_y[ya, xa] + d)
        pixels_y[yb, xb] = max(0, pixels_y[yb, xb] - d)
        
    new_y = Image.fromarray(pixels_y.astype(np.uint8))
    stego_img = Image.merge('YCbCr', (new_y, cb, cr)).convert('RGB')
    stego_img.save(output_path)

def detect_patchwork(image_path, seed, n_pairs, threshold):
    img = Image.open(image_path).convert('YCbCr')
    
    y, _, _ = img.split()
    
    pixels_y = np.array(y, dtype=np.int32)
    width, height = img.size
    
    pairs = generate_pairs(seed, n_pairs, width, height)
    
    #suma różnic jasności S spodziewana 2*N_PAIRS*D=60000
    S = 0
    for a, b in pairs:
        xa, ya = a
        xb, yb = b
        S += (pixels_y[ya, xa] - pixels_y[yb, xb])
        
    print(f"Suma roznic (S) = {S}")
    
    if S > threshold:
        print("--> Wykryto znak wodny!")
        return True
    else:
        print("--> Nie wykryto znaku wodnego.")
        return False


def generate_difference_map(original_path, watermarked_path, diff_map_path, gain=10):
    img_orig = Image.open(original_path).convert('L')
    img_stego = Image.open(watermarked_path).convert('L')
    
    arr_orig = np.array(img_orig, dtype=np.int32)
    arr_stego = np.array(img_stego, dtype=np.int32)
    

    diff = arr_stego - arr_orig
    visual_diff = 128 + (diff * gain)
    
    visual_diff = np.clip(visual_diff, 0, 255).astype(np.uint8)
    Image.fromarray(visual_diff).save(diff_map_path)
    print(f"Mapa różnic zapisana jako: {diff_map_path}")

if __name__ == "__main__":
    print("=== Znak Wodny Patchwork ===")
    
    PLIK_WEJSCIOWY = "las.png"
    PLIK_WYJSCIOWY = "las_watermarked.png"

    # Parametry algorytmu
    SEED = 12345
    N_PAIRS = 10000
    D = 3
    
    THRESHOLD = N_PAIRS * D
    
    print("\n--- Test oryginalnego obrazu (przed dodaniem znaku) ---")
    detect_patchwork(PLIK_WEJSCIOWY, SEED, N_PAIRS, THRESHOLD)
    
    print("\n--- Osadzanie znaku wodnego ---")
    embed_patchwork(PLIK_WEJSCIOWY, PLIK_WYJSCIOWY, SEED, N_PAIRS, D)
    
    print("\n--- Test obrazu ze znakiem wodnym (poprawny klucz) ---")
    detect_patchwork(PLIK_WYJSCIOWY, SEED, N_PAIRS, THRESHOLD)
    
    print("\n--- Test obrazu ze znakiem wodnym (falszywy klucz) ---")
    detect_patchwork(PLIK_WYJSCIOWY, 99999, N_PAIRS, THRESHOLD)
    
    generate_difference_map(PLIK_WEJSCIOWY, PLIK_WYJSCIOWY, "las_diff.png")
