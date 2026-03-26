# Podstawy Ochrony Danych - laboratorium AGC

## BBS - Implementacja generatora ciągów losowych oraz wybranych testów losowości

### Algorytm

1. Wyznacz wartość iloczynu N dwóch dużych liczb pierwszych, takich że:
   $p \equiv 3 \bmod 4$
   $q \equiv 3 \bmod 4$
2. Wybierz w sposób losowy taką liczbę x taką, że x i N są względnie pierwsze.
3. Wyznacz wartość pierwotną generatora:
   $x_0 = x^2 \bmod N$
4. Powtarzaj w pętli:
   $x_{i+1} = x_i^2 \bmod N$

Bit wyjścia stanowi najmłodszy bit (LSB, ang. *Least Significant Bit*) będący jednocześnie i-tym bitem klucza.

---

**Cel ćwiczenia laboratoryjnego:** zapoznanie się z tematyką generatorów ciągów pseudolosowych, analiza własności jakie powinny posiadać takie ciągi, implementacja generatora BBS oraz 4 testów FIPS 140-2 (pojedynczych bitów, długiej serii, serii oraz pokerowego).