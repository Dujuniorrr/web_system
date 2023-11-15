# import pandas as pd
# import urllib.request
# import re
# import sqlite3
# from bs4 import BeautifulSoup

# site="http://tempo.cptec.inpe.br/ba/livramento"   
# with urllib.request.urlopen(site) as url:
#     page = url.read()
# soup = BeautifulSoup(page,"html.parser")
# dados00 = soup.find_all('div',attrs={'class': 'previsao'})
# dados01 = soup.find_all('div',attrs={'class': 'proximos-dias'})

# count=0
# weekPrediction=[]
# df = pd.DataFrame
# today = dados00[0].get_text().split()[1]
# dayPredictionList=[]
# weekPrediction=[]
# count=0
# df = pd.DataFrame

# for data in dados00:
#     dataA = data.get_text().split()
#     dataB = dataA[1:2]+[dataA[-6]]+[dataA[-7]]+[dataA[-3]]+[max([dataA[3],dataA[5],dataA[7]])]+dataA[-2:]
#     dayPredictionList=dataB
#     dayPredictionList.append(today)
#     dayPredictionList.append(str(count))
#     weekPrediction.append(dayPredictionList)
#     count+=1
# dayPredictionList.clear

# for data in dados01:
#     dataA = data.get_text().split()
#     dataB = dataA[1:2]+[dataA[2]]+[dataA[3]]+[dataA[6]]+[dataA[-3]]+dataA[-2:]
#     dayPredictionList=dataB
#     dayPredictionList.append(today)
#     dayPredictionList.append(str(count))
#     weekPrediction.append(dayPredictionList)
#     count+=1
    
# print(weekPrediction)
# # stmt = "INSERT INTO WEATHER VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
# # con.executemany(stmt, weekPrediction)
# # con.commit()

import cssutils

# CSS de exemplo
css_text = """
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}

h1 {
    color: blue;
}

p, h2 {
    font-size: 16px;
}
"""

# Analisar o CSS
css_parser = cssutils.CSSParser()
stylesheet = css_parser.parseString(css_text)

# Iterar pelas regras CSS e imprimir informações
for rule in stylesheet:
    if rule.type == rule.STYLE_RULE:
        selector_text = rule.selectorText
        declarations = rule.style
        print(f"Seletor: {selector_text}")
        for prop in declarations:
            print(f"   {prop.name}: {prop.value}")
