"""
Een vriend heeft een boete gereden in Duitsland
Daar ging hij 25 km/u te hard en moest 115 euro betalen
In Nederland zou dat 336 euro zijn

Hoeveel geld per uur moet je verdienen om de tijdswinst met de 25 km/u te rechtvaardigen?

We gaan uit van de volgende situatie

- we leggen 200 km af
- de max snelheid is 130 km/u
- wij gaan dus 155 km/u


hoeveel geld moet je verdienen om de tijdswinst het waard te maken t.o.v de boete?
(op een rit van 200km waarbij we 25 km/u te hard rijden op een snelweg waar je max 130 km/u mag en we krijgen maar 1 boete)
"""

import matplotlib.pyplot as plt

boete_kosten_NL = 336  # euro
boete_kosten_DE = 115  # euro

max_snelheid = 100  # km / uur
huidige_snelheid = 125  # km / uur
gebruikelijke_afstand = 200  # km

gebruikelijke_tijdsduur = gebruikelijke_afstand / max_snelheid
huidige_tijdsduur = gebruikelijke_afstand / huidige_snelheid
tijdswinst = gebruikelijke_tijdsduur - huidige_tijdsduur

inkomsten = range(30, 2000, 10)   # inkomsten euro / uur
netto_kosten_NL = [boete_kosten_NL - tijdswinst * x for x in inkomsten]
netto_kosten_DE = [boete_kosten_DE - tijdswinst * x for x in inkomsten]

nulpunt_NL = boete_kosten_NL / tijdswinst
nulpunt_DE = boete_kosten_DE / tijdswinst

fig, ax = plt.subplots(1)
fig.suptitle(f"Afstand: {gebruikelijke_afstand} km, max snelheid: {max_snelheid} km/u, huidige snelheid: {huidige_snelheid} km/u")
ax.plot(inkomsten, netto_kosten_NL, label='NL')
ax.plot(inkomsten, netto_kosten_DE, label='DE')
ax.scatter(nulpunt_NL, 0, marker="o")
ax.scatter(nulpunt_DE, 0, marker="o")
ax.text(nulpunt_NL, 2, f"Nulpunt NL: {int(nulpunt_NL)}")
ax.text(nulpunt_DE, -4, f"Nulpunt DE: {int(nulpunt_DE)}")
ax.hlines(0, inkomsten[0], inkomsten[-1], 'k', label='break-even')
ax.set_xlabel("Inkomsten per uur")
ax.set_ylabel("Netto kosten")
ax.set_ylim(-50, 50)
plt.legend()
fig.savefig("dundundun_100.png")


# Plot in duitsland vs nederland bij variabele inkomsten
#