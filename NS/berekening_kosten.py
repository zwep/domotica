
"""
Tarief Houten - Eindhoven

aantal eenheden bepaalt via

https://www.ns.nl/binaries/_ht_1607588395551/content/assets/ns-nl/tarieven/tariefeenhedenkaart-van-nederland-2021.pdf

prijzen via

https://www.ns.nl/binaries/_ht_1641394414516/content/assets/ns-nl/tarieven/2022/ns-tarievenlijst-2022.pdf
https://email.ns.nl/images/NS/Campagnes/C12852/ns-tarievenlijst-consumenten-2023.pdf
"""
import numpy as np
import matplotlib.pyplot as plt

N = 20
n_trips = np.arange(0, 2*N, 2)
y1 = 107.90  # DAL vrij
y2 = 8.70 * n_trips + 5.10  # 40% korting
y3 = 14.50 * n_trips  # geen

y2_crossing = np.round((y1 - 5.10) / 8.70, 1)
y3_crossing = np.round(y1 / 14.50, 1)

fig, ax = plt.subplots(2)
ax[0].hlines(y1, 0, 2*N, label='DAL vrij', color='k')
ax[0].plot(n_trips, y2, label='40% korting')
ax[0].plot(n_trips, y3, label='geen abbo')
ax[0].legend()
ax[0].set_xlabel('Aantal ritten per maand')
ax[0].set_ylabel('Kosten per maand')
ax[0].set_title('Kosten overzicht tussen Houten en Eindhoven 2022')
ax[0].scatter(x=y2_crossing, y=y1, c='r', marker='o')
ax[0].text(s=y2_crossing, x=y2_crossing, y=y1+5)
ax[0].scatter(x=y3_crossing, y=y1, c='r', marker='o')
ax[0].text(s=y3_crossing, x=y3_crossing, y=y1+5)

N = 20
n_trips = np.arange(0, 2*N, 2)
y1 = 119.95  # DAL vrij
y2 = 9.18 * n_trips + 5.60  # 40% korting
y3 = 15.30 * n_trips  # geen
y2_crossing = np.round((y1 - 5.60) / 9.18, 1)
y3_crossing = np.round(y1 / 15.30, 1)

ax[1].hlines(y1, 0, 2*N, label='DAL vrij', color='k')
ax[1].plot(n_trips, y2, label='40% korting')
ax[1].plot(n_trips, y3, label='geen abbo')
ax[1].legend()
ax[1].set_xlabel('Aantal ritten per maand')
ax[1].set_ylabel('Kosten per maand')
ax[1].set_title('Kosten overzicht tussen Houten en Eindhoven 2023')
ax[1].scatter(x=y2_crossing, y=y1, c='r', marker='o')
ax[1].text(s=y2_crossing, x=y2_crossing, y=y1+5)
ax[1].scatter(x=y3_crossing, y=y1, c='r', marker='o')
ax[1].text(s=y3_crossing, x=y3_crossing, y=y1+5)