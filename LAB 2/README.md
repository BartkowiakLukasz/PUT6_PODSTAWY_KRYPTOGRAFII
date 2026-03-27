# Generowanie kluczy (Algorytm RSA)

Poniższa tabela przedstawia kolejne kroki niezbędne do wygenerowania kluczy kryptograficznych:

| Czynność |
| :--- |
| Wybieramy dwie liczby pierwsze `p` i `q` |
| Obliczamy `n = p * q` |
| Obliczamy `phi = (p - 1)(q - 1)` |
| Generujemy `e` jako liczbę względnie pierwszą z `phi`, czyli taką, która jest liczbą pierwszą i dla której największy wspólny dzielnik z `phi` wynosi 1 |
| Generujemy `d` w taki sposób, aby spełniona była zależność: iloczyn `e` i `d` przystaje do 1 modulo `phi`. Co oznacza, że `phi` dzieli wyrażenie `e * d - 1`. |  
Para `e` i `n` stanowią klucz publiczny, natomiast para `d` i `n` jest kluczem prywatnym.

### Szyfrowanie wiadomości:

| Czynność |
| :--- |
| `c = m ^ e mod n`; gdzie `c` oznacza wiadomość zaszyfrowaną, a `m` wiadomość jawną. |

### Deszyfrowanie wiadomości:

| Czynność |
| :--- |
| `m = c ^ d mod n`; gdzie `c` oznacza wiadomość zaszyfrowaną, a `m` wiadomość jawną. |  

# Algorytm Diffiego-Hellmana

**Zadanie:**

Algorytm Diffiego-Helmana oparty jest na trudności obliczania logarytmów dyskretnych w ciałach skończonych. Wykorzystywany jest do dystrybucji kluczy (nie do szyfrowania i deszyfrowania).

### Algorytm:
1. A i B uzgadniają ze sobą w sposób jawny wybór dwóch dużych liczb całkowitych **`n`** – duża liczba pierwsza i **`g`** – pierwiastek pierwotny modulo `n`, gdzie `1 < g < n`.
2. A wybiera losową dużą liczbę całkowitą `x` (tajną) – to będzie jej klucz prywatny i oblicza `X = g^x mod n`.
3. B wybiera losową dużą liczbę całkowitą `y` (tajną) – to będzie klucz prywatny osoby B i oblicza `Y = g^y mod n`.
4. A i B przesyłają do siebie nawzajem obliczone `X` i `Y`.
5. A oblicza `k = Y^x mod n`.
6. B oblicza `k = X^y mod n`.
7. Mogą teraz używać `k` jako klucza sesji (np. do algorytmu blokowego).