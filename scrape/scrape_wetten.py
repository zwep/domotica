"""Overheid wetten """

import requests
from bs4 import BeautifulSoup


def haal_artikel_op(wetboek, artikel_nummer):
    url = f"https://wetten.overheid.nl/BWBR0001903/2022-01-01#Boek2_TiteldeelI_Artikel{artikel_nummer}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Vind het element met de tekst van het artikel
    artikel_element = soup.find("div", {"id": f"artikel_{artikel_nummer}"})

    if artikel_element:
        artikel_tekst = artikel_element.text.strip()
        print(f"Artikel {artikel_nummer} van {wetboek}:\n{artikel_tekst}")
    else:
        print(f"Artikel {artikel_nummer} niet gevonden in {wetboek}.")


# Voorbeeld: Artikel 27 van het Wetboek van Strafvordering
haal_artikel_op("Wetboek van Strafvordering", 27)

artikel_nummer = 27
url = "https://wetten.overheid.nl/jci1.3:c:BWBR0001903&boek=Eerste&titeldeel=II&artikel=27&z=2023-03-01&g=2023-03-01"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Vind het element met de tekst van het artikel
artikel_element = soup.find("div", {"id": f"artikel_{artikel_nummer}"})

soup.text
