
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Obter o diretório onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(script_dir, "datasets")
os.makedirs(datasets_dir, exist_ok=True)

# ----------------------------
# 1. Titanic (simulado)
# ----------------------------
np.random.seed(42)
titanic = pd.DataFrame({
    'PassengerId': range(1, 501),
    'Pclass': np.random.choice([1, 2, 3], 500, p=[0.2, 0.3, 0.5]),
    'Sex': np.random.choice(['male', 'female'], 500),
    'Age': np.random.normal(30, 14, 500).clip(1, 80),
    'Fare': np.random.uniform(10, 150, 500),
    'Survived': np.random.choice([0, 1], 500, p=[0.6, 0.4])
})
titanic.to_csv(os.path.join(datasets_dir, "titanic.csv"), index=False)

# ----------------------------
# 2. Vendas corporativas
# ----------------------------
datas = pd.date_range(start="2022-01-01", end="2024-12-31", freq="M")
produtos = ['Notebook', 'Smartphone', 'Impressora', 'Monitor', 'Headset']
regioes = ['Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Norte']
vendedores = ['Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda']

registros = []
for data in datas:
    for regiao in regioes:
        for produto in produtos:
            vendedor = np.random.choice(vendedores)
            vendas = np.random.randint(5, 100)
            preco = np.random.uniform(500, 5000)
            receita = vendas * preco
            custo = receita * np.random.uniform(0.5, 0.8)
            registros.append([data, regiao, produto, vendedor, vendas, round(receita,2), round(custo,2)])

vendas_df = pd.DataFrame(registros, columns=['Data', 'Regiao', 'Produto', 'Vendedor', 'Qtd_Vendida', 'Receita', 'Custo'])
vendas_df['Lucro'] = vendas_df['Receita'] - vendas_df['Custo']
vendas_df.to_csv(os.path.join(datasets_dir, "vendas.csv"), index=False)

# ----------------------------
# 3. IBGE População (simulado)
# ----------------------------
anos = range(2015, 2025)
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
ibge = pd.DataFrame({
    'Ano': np.repeat(list(anos), len(regioes)),
    'Regiao': regioes * len(anos),
    'Populacao': np.random.randint(1_000_000, 30_000_000, len(anos)*len(regioes))
})
ibge.to_csv(os.path.join(datasets_dir, "ibge_populacao.csv"), index=False)

# ----------------------------
# 4. COVID (simulado)
# ----------------------------
datas = pd.date_range(start="2020-03-01", end="2022-12-31", freq="W")
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
covid = []
for data in datas:
    for regiao in regioes:
        casos = np.random.randint(100, 5000)
        obitos = np.random.randint(0, int(casos * 0.05))
        vacinados = np.random.randint(int(casos * 0.2), int(casos * 0.9))
        covid.append([data, regiao, casos, obitos, vacinados])
covid_df = pd.DataFrame(covid, columns=['Data', 'Regiao', 'Casos', 'Obitos', 'Vacinados'])
covid_df.to_csv(os.path.join(datasets_dir, "covid.csv"), index=False)

# ----------------------------
# 5. Filmes (simulado)
# ----------------------------
filmes = pd.DataFrame({
    'Filme': [f'Filme_{i}' for i in range(1, 201)],
    'Genero': np.random.choice(['Ação', 'Comédia', 'Drama', 'Terror', 'Ficção'], 200),
    'Ano': np.random.randint(1990, 2024, 200),
    'Nota': np.random.uniform(1, 10, 200).round(1),
    'Popularidade': np.random.randint(100, 10000, 200)
})
filmes.to_csv(os.path.join(datasets_dir, "filmes.csv"), index=False)

print(f"✅ Datasets gerados com sucesso em: {datasets_dir}")