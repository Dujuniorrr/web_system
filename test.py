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

# import cssutils

# # CSS de exemplo
# css_text = """
# body {
#     font-family: Arial, sans-serif;
#     background-color: #f0f0f0;
# }

# h1 {
#     color: blue;
# }

# p, h2 {
#     font-size: 16px;
# }
# """

# # Analisar o CSS
# css_parser = cssutils.CSSParser()
# stylesheet = css_parser.parseString(css_text)

# # Iterar pelas regras CSS e imprimir informações
# for rule in stylesheet:
#     if rule.type == rule.STYLE_RULE:
#         selector_text = rule.selectorText
#         declarations = rule.style
#         print(f"Seletor: {selector_text}")
#         for prop in declarations:
#             print(f"   {prop.name}: {prop.value}")

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Exemplo de dados (substitua pelos seus dados reais)
# data = {
#     'pests_number': [10, 15, 8, 12, 18, 22, 25, 30, 28, 35, 40, 45, 50, 55, 58, 60],
#     'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05',
#                             '2023-01-06', '2023-01-07', '2023-01-08', '2023-01-09', '2023-01-10',
#                             '2023-01-11', '2023-01-12', '2023-01-13', '2023-01-14', '2023-01-15', '2023-01-16']),
#     'temperature': [25.5, 24.8, 26.0, 25.2, 27.0, 28.5, 29.0, 30.2, 28.8, 31.5, 32.0, 33.5, 34.0, 35.2, 36.0, 37.5],
#     'pressure': [1012.0, 1010.5, 1013.2, 1011.8, 1014.5, 1016.0, 1015.5, 1017.2, 1016.0, 1018.5, 1019.0, 1020.5, 1021.0, 1022.2, 1023.0, 1024.5],
# }

# df = pd.DataFrame(data)

# # Gráfico de dispersão entre número de pragas e temperatura
# plt.figure(figsize=(12, 6))
# plt.subplot(2, 2, 1)
# sns.scatterplot(x='temperature', y='pests_number', data=df)
# plt.title('Número de Pragas vs. Temperatura')

# # Gráfico de dispersão entre número de pragas e pressão atmosférica
# plt.subplot(2, 2, 2)
# sns.scatterplot(x='pressure', y='pests_number', data=df)
# plt.title('Número de Pragas vs. Pressão Atmosférica')

# # Gráfico de dispersão entre número de pragas e data
# plt.subplot(2, 2, 3)
# sns.lineplot(x='date', y='pests_number', data=df)
# plt.title('Número de Pragas ao longo do Tempo')
# plt.xticks(rotation=45)

# # Gráfico de dispersão entre temperatura e pressão atmosférica
# plt.subplot(2, 2, 4)
# sns.scatterplot(x='temperature', y='pressure', data=df)
# plt.title('Temperatura vs. Pressão Atmosférica')

# plt.tight_layout()
# plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Dados de exemplo
temperatura = [25.5, 24.8, 26.0, 25.2, 28.5, 28.5, 28.5, 28.5, 28.5, 31.5, 32.0, 33.5, 34.0, 35.2, 36.0, 37.5]  # Substitua pelo seu conjunto de dados real
num_pragas = [10, 15, 8, 12, 18, 22, 22, 22, 22, 22, 22, 45, 50, 55, 58, 60]    # Substitua pelo seu conjunto de dados real
pressao_atmosferica = np.random.uniform(1000, 1020, 50)  # Substitua pelo seu conjunto de dados real

# Criar o Gráfico de Dispersão com Correlações
plt.scatter(temperatura, num_pragas, cmap='viridis', alpha=0.8)


# Adicionar rótulos e título
plt.xlabel('Temperatura')
plt.ylabel('Número de Pragas')
plt.title('Gráfico de Dispersão com Correlações')

# # Adicionar barra de cores indicando a pressão atmosférica
# barra_cores = plt.colorbar()
# barra_cores.set_label('Pressão Atmosférica')

# Exibir o gráfico
plt.show()
