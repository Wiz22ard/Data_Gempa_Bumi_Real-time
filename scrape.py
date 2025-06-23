# scrape.py
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4

dfPast = pd.read_csv('gempa_realtime.csv')

r = requests.get('https://www.bmkg.go.id/gempabumi/gempabumi-realtime')
s = bs4(r.text, 'html.parser')
t = s.find('tbody')

rows = []
for tr in t.find_all('tr'):
    tds = tr.find_all('td')
    tanggal = tds[1].text[:11].strip()
    waktu = tds[1].text[11:].split('.')[0].strip()
    magnitudo = float(tds[2].text.strip().replace(',', '.'))
    kedalaman = int(tds[3].text.strip().split(' ')[0])
    koordinat = tds[4].text.strip().replace(' LS', '').replace(' LU', '').replace(' BT', '').replace(',', '.').replace('-', ',')
    wilayah = tds[5].text.strip()

    match = ((dfPast['Tanggal'] == tanggal) & (dfPast['Waktu (WIB)'] == waktu)).any()
    if not match:
        rows.append([tanggal, waktu, magnitudo, kedalaman, koordinat, wilayah])

if rows:
    dfNew = pd.DataFrame(rows, columns=dfPast.columns)
    dfCombined = pd.concat([dfPast, dfNew], ignore_index=True)
    dfCombined.to_csv('gempa_realtime.csv', index=False)
    print(f"{len(rows)} data baru ditambahkan")
else:
    print("Tidak ada data baru")
