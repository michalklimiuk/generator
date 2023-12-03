import math

class SystemMG1:
    def __init__(self):
        self.bufor = []
        self.czasy_obslugi = []
        self.stan_losowy = 42  # seed - początkowy stan generatora liczb pseudolosowych

    def generuj_losowa(self):
        self.stan_losowy = (self.stan_losowy * 1664525 + 1013904223) % (2**32)
        return self.stan_losowy / (2**32)

    def generuj_przybycie(self):
        return -120 * math.log(self.generuj_losowa())

    def generuj_czas_obslugi(self, rozklad):
        if rozklad == 'staly':
            return 60
        elif rozklad == 'jednostajny':
            return self.generuj_losowa() * 120
        elif rozklad == 'wykladniczy':
            return -60 * math.log(self.generuj_losowa())
        elif rozklad == 'normalny':
            z1 = self.generuj_losowa()
            z2 = self.generuj_losowa()
            return max(0, math.sqrt(-2 * math.log(z1)) * math.cos(2 * math.pi * z2) * 20 + 60)
        else:
            raise ValueError("Nieprawidłowy typ rozkładu")

    def symuluj(self, liczba_iteracji, rozklad_obslugi):
        calkowity_czas_w_buforze = 0

        for _ in range(liczba_iteracji):
            czas_przybycia = self.generuj_przybycie()

            # obsługa przybycia i odejścia
            if not self.bufor:  # bufor jest pusty obsługa zaczyna się od razu
                czas_obslugi = self.generuj_czas_obslugi(rozklad_obslugi)
                czas_odjazdu = czas_przybycia + czas_obslugi
                calkowity_czas_w_buforze += czas_obslugi
            else:   # bufor nie jest pusty, dodaj przybycie do kolejki
                self.bufor.append(czas_przybycia)
                continue

            while self.bufor and self.bufor[0] < czas_odjazdu:  # sprawdzenie czy są oczekujące przybycia w buforze
                # obsługa następnego przybycia w buforze
                czas_przybycia = self.bufor.pop(0)
                czas_obslugi = self.generuj_czas_obslugi(rozklad_obslugi)
                czas_odjazdu = czas_przybycia + czas_obslugi
                calkowity_czas_w_buforze += (czas_odjazdu - czas_przybycia)

            # wypisz wyniki dla każdego przypadku
            print(f"Przypadek {rozklad_obslugi}: Przybycie: {czas_przybycia:.2f}, Obsługa: {czas_obslugi:.2f}, Odjazd: {czas_odjazdu:.2f}")

        # oblicz średni czas w buforze
        sredni_czas_w_buforze = calkowity_czas_w_buforze / liczba_iteracji
        return sredni_czas_w_buforze

system = SystemMG1()
# for typ_rozkladu in ['staly', 'jednostajny', 'wykladniczy', 'normalny']:
#     sredni_czas = system.symuluj(1000000, typ_rozkladu)
#     print(f"Średni czas przebywania zgłoszenia w buforze ({typ_rozkladu}): {sredni_czas:.2f} sekundy")

sredni_czas = []
for i, rozklad in enumerate(['staly', 'jednostajny', 'wykladniczy', 'normalny']):
    sredni_czas.append(system.symuluj(1000, rozklad))
print(f"Średni czas przebywania zgłoszenia w buforze dla rozkładu [stały, jednostajny, wykładniczy, normalny]: {sredni_czas}")

