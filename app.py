# Projeto Com DataSet Netflix do pandas
import pandas 
import datetime
import matplotlib.pyplot as plt
#criando o dataframe
df = pandas.read_csv("netflix_titles.csv", index_col="show_id")

# 1.1 - Limpeza e preparação dos dados
df.dropna(inplace=True) # removeno linha com valores NA

df["date_added"] = pandas.to_datetime(df["date_added"].str.strip() ,errors="coerce") # convertendo a coluna date_added para o formato datetime


# 1.2 - Tratando colunas com múltiplos valores separados por vírgula
df["country"] = df["country"].str.split(", ")
df["country"].explode() # separando os países em linhas diferentes
df["listed_in"] = df["listed_in"].str.split(", ")
df["listed_in"].explode() # separando os gêneros em linhas diferentes
df["cast"] = df["cast"].str.split(", ")
df["cast"].explode() # separando os atores em linhas diferentes

# 1.3 - Criando colunas auxiliares
df["year_added"] = df["date_added"].dt.year # criando uma nova coluna com o ano de adição
df["month_added"] = df["date_added"].dt.month # criando uma nova coluna com
df["release_on_netlix_diference"] = df["year_added"] - df["release_year"] # criando uma nova coluna com o ano de lançamento na netflix


#2.0 - Análise exploratória dos dados

#2.1 - Visualização da quantidade de filmes e séries na Netflix
novoDf = df["type"].groupby(df["type"]).size().reset_index(name="count")
novoDf.plot(
    x = "type",
    y = "count",
    kind = "bar",
    title= "Quantidade de Filmes e Séries na Netflix",
    color = ["blue", "orange"],
    legend= False,
    width = 0.2,
)
plt.xlabel("Tipo", fontsize= 12, fontweight= "bold")
plt.ylabel("Quantidade", fontsize= 12, fontweight= "bold")
plt.yticks(range(0, 6000, 500))
plt.tight_layout()
# plt.show()

#2.2 - Visualização da quantidade de lançamentos por ano
novoDf2 = df["year_added"].groupby(df["year_added"]).size().sort_index().reset_index(name="count")

novoDf2.plot(
    x = "year_added",
    y = "count",
    kind = "line",
    marker = "o",
    title = "Quantidade de lançamentos por ano",
    color = "green",
    legend=False
)
plt.xlabel("Ano de lançamento", fontsize= 12, fontweight= "bold")
plt.ylabel("Quantidade de lançamentos na Netlix", fontsize= 12, fontweight= "bold")
plt.grid(True)
plt.yticks(range(0, novoDf2["count"].max() +100, 100))
plt.xticks(range(2005, 2025, 1), rotation=45, ha = 'right')
plt.tight_layout()
plt.show()





