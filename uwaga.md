## ⚠️ Uwaga – na co trzeba uważać przy próbie budowy lampki fotonowej

Ten projekt opisuje **model topologiczny**, a nie gotowy, zweryfikowany układ laboratoryjny.  
Przy próbie fizycznej realizacji szczególnie ważne są następujące punkty:

### 1. Geometria cewek (skręt pola)

- **Kierunek nawinięcia:**  
  Cewki muszą mieć **jednoznacznie przeciwny skręt** (A i B). „Prawie tak samo” = klasyczny transformator, nie układ skrętowy.
- **Symetria:**  
  Zbyt duża asymetria liczby zwojów, średnicy lub długości → dominuje zwykłe sprzężenie indukcyjne, a nie efekt skrętu.
- **Położenie w przestrzeni:**  
  Za blisko → klasyczne sprzężenie, za daleko → brak realnej różnicy pola.  
  Geometria układu ma krytyczne znaczenie.

### 2. Strojenie rezonansu

- **Częstotliwość pracy:**  
  Rezonans musi być dobrany tak, aby układ „żył” – poza zakresem rezonansu zobaczymy tylko straty i szum.
- **Jakość Q układu:**  
  Zbyt niskie Q → efekt się rozmywa.  
  Zbyt wysokie Q → układ może być niestabilny, łatwo o wzbudzenia w niepożądanych pasmach.
- **Elementy pasożytnicze:**  
  Pojemności przewodów, indukcyjności połączeń, masa stołu, ekranowanie – wszystko to może zabić subtelny efekt skrętu.

### 3. Iluzje pomiarowe i „fałszywe świecenie”

- **Zakłócenia RF i sieciowe:**  
  LED potrafi świecić od śmieci wysokoczęstotliwościowych, ładunków pojemnościowych czy indukcji z sieci – to nie musi być efekt skrętu.
- **Czujniki optyczne:**  
  Fotodiody, fototranzystory, kamery – rejestrują także szum, odbicia i zakłócenia.  
  Potrzebne są **powtarzalne, kontrolowane pomiary**, a nie pojedyncze „dziwne zjawiska”.
- **Zasilacze impulsowe:**  
  Mogą wprowadzać widmo zakłóceń, które wygląda jak „sygnał”, a jest tylko brudem z przetwornicy.

### 4. Bezpieczeństwo

- **Napięcia i prądy:**  
  Przy wyższych napięciach konieczna jest dbałość o izolację, odstępy, uziemienie i chłodzenie elementów.
- **Silne pola EM:**  
  Długotrwała praca przy silnych polach może być uciążliwa (ból głowy, szum w uszach).  
  Warto ograniczać moc do minimum i stosować ekranowanie.
- **Przegrzewanie elementów:**  
  Cewki, rdzenie, kondensatory mogą się nagrzewać nawet przy pozornie małej mocy – wymagają kontroli temperatury.

### 5. Interpretacja wyników

- **Brak efektu ≠ zły model:**  
  Możliwa jest zła częstotliwość, niewłaściwa geometria, zbyt mała różnica skrętów lub zbyt duże straty w układzie.
- **Efekt bardzo słaby na początku:**  
  Pierwsze realizacje mogą dawać **minimalne, ledwo mierzalne** efekty – łatwe do pomylenia z szumem lub zignorowania.
- **Uczciwość wobec danych:**  
  Niezależnie od oczekiwań – liczy się powtarzalny, mierzalny wynik.  
  Ten projekt ma charakter **badawczy**, a nie gwarancję działania konkretnej konstrukcji.

