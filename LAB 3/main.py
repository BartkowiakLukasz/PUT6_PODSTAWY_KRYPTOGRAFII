import hashlib
import time
if __name__ == "__main__":
   #print(hashlib.algorithms_available())
    HASHES = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
    print(HASHES)
    test_txt = ["Kot", "To jest testowe zdanie do sprawdzenia funkcji skrótu.", "Pierwszym śladem człowieka na terytorium dzisiejszego Iranu są rysunki naskalne w pieczarze w Ghonbad-e Kus w Mazandaranie, datowane na 40 tys. lat p.n.e., przedstawiające polowanie na niedźwiedzie, nosorożce i dziki. W XI tysiącleciu p.n.e. istniały już na tym obszarze ludzkie osady, zaś z połowy IX tysiąclecia p.n.e. pochodzi osada z Gandż Dare, której mieszkańcy trudnili się hodowlą i prymitywnym rolnictwem. Następnie w całym Iranie nastąpiły rozwój kultur neolitycznych i związana z nim ekspansja osadnictwa. Pierwszym państwem na terenie Iranu był Elam, zajmujący w przybliżeniu terytorium dzisiejszego ostanu Chuzestan, którego stolica, Suza, została założona już ok. 4200 roku p.n.e. Przełomowym wydarzeniem w historii Iranu było przybycie na jego terytorium Ariów, przodków dzisiejszych Irańczyków, pod koniec II tysiąclecia p.n.e. Początkowo najpotężniejszym z ich plemion byli Medowie, którzy pod koniec VII w. p.n.e. zniszczyli państwo asyryjskie i założyli własne imperium, rozciągające się od Lidii na zachodzie do Baktrii na wschodzie. Ich państwo przejął jednak ok. roku 550 p.n.e. w wyniku buntu władca Persów z dynastii Achemenidów Cyrus II (559–529 p.n.e.). Wkrótce podbił on Lidię i Babilonię, a jego następcy rozciągnęli władzę Achemenidów także na Egipt i dolinę Indusu. Imperium Achemenidów było szczytowym momentem politycznej potęgi Irańczyków w całej ich historii."]
    for txt in test_txt:
      txt = txt.encode('utf-8')
      results = []
      for name in HASHES:
         start = time.perf_counter()
         algorithm = hashlib.new(name)
         algorithm.update(txt)
         algorithm_hex = algorithm.hexdigest()
         end = time.perf_counter()
         total_time = (end - start) * 10**6
         print(f"HASH of {name}: {algorithm_hex}")
         print(f"Total time: {total_time} mu, len = {len(algorithm_hex)}")
         results.append((name, total_time, len(algorithm_hex))) 
      print("----------------------------------------------------------")
      print(f"Diff in elapsed time and output lenght of {len(txt)} input lenght")
      fastest = min(results, key= lambda x: x[1])
      print(f"The fastest algorithm: {fastest[0]}, {fastest[1]} mu")
      slowest = max(results, key = lambda x : x[1])
      print(f"The slowest algorithm: {slowest[0]}, {slowest[1]} mu")
      shortest = min(results, key = lambda x : x[2])
      print(f"The shortest output: {shortest[0]}, {shortest[2]}")
      longest = max(results, key = lambda x : x[2])
      print(f"The longest output: {longest[0]}, {longest[2]}")
      print("----------------------------------------------------------")
      print("\n\n")
    