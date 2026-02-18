# Projeto Com DataSet Netflix do pandas
import pandas 
import datetime
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
#criando o dataframe
df = pandas.read_csv("netflix_titless.csv")

# 1.1 - Limpeza e preparação dos dados
df.dropna(subset=['title', 'date_added'], inplace=True) # removeno linha com valores NA

df["date_added"] = pandas.to_datetime(df["date_added"].str.strip() ,errors="coerce") # convertendo a coluna date_added para o formato datetime


# 1.2 - Tratando colunas com múltiplos valores separados por vírgula
df["country"] = df["country"].str.split(", ")
df = df.explode("country").reset_index(drop=True) # separando os países em linhas diferentes
df["listed_in"] = df["listed_in"].str.split(", ")
df = df.explode("listed_in").reset_index(drop=True) # separando os gêneros em linhas diferentes
df["cast"] = df["cast"].str.split(", ")
df = df.explode("cast").reset_index(drop=True) # separando os atores em linhas diferentes

# 1.3 - Criando colunas auxiliares
df["year_added"] = df["date_added"].dt.year # criando uma nova coluna com o ano de adição
df["month_added"] = df["date_added"].dt.month # criando uma nova coluna com
df["release_on_netlix_diference"] = df["year_added"] - df["release_year"] # criando uma nova coluna com o ano de lançamento na netflix


#2.0 - Análise exploratória dos dados

#2.1 - Visualização da quantidade de filmes e séries na Netflix
novoDf = df.groupby("type")["show_id"].nunique().reset_index(name="count")
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

#2.2.1 - Identificação de picos de crescimento(titulos adicionados por ano)
titles_by_year = df.groupby("year_added")["show_id"].nunique().sort_index()
diference = titles_by_year.diff()
peak_year = diference.idxmax()
peak_value = diference.max()
# print(f"O pico de crescimento ocorreu em {peak_year} com um aumento de {peak_value} títulos em relação ao ano anterior.")   

#2.2.2 - Visualização do crescimento de títulos por ano
novoDf2 = df.groupby("year_added")["show_id"].nunique().sort_index().reset_index(name="count")

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
plt.axvline(peak_year, linestyle= "--")
# plt.show()

#2.3 - Visualização da quantidade de títulos adicionados por mês
titles_add_by_month = df.groupby("month_added")["show_id"].nunique().reset_index(name="count")
titles_add_by_month["month_added"]= ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

titles_add_by_month.plot(
    x="month_added",
    y="count",
    kind="bar",
    color= "purple",
    legend=False,
    title = "Quantidade de titulos adicionados por mes"
)
plt.xlabel("Mês de adição", fontsize= 12, fontweight= "bold")
plt.ylabel("Quantidade de títulos adicionados", fontsize= 12, fontweight= "bold")
plt.tight_layout()
# plt.show() 

#2.4 - Top 10 países com mais títulos na Netflix
titles_by_contry = df.groupby("country")["show_id"].nunique().reset_index(name="count").sort_values(by="count", ascending=False)

titles_by_contry.head(10).plot(
    x= "country",
    y="count",
    kind="bar",
    title="Top 10 países com mais títulos na Netflix",
    color = 'cyan',
    legend=False
)

plt.xlabel("País", fontsize= 12, fontweight= "bold")
plt.ylabel("Quantidade de títulos", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
# plt.show()

#Top 10 países com mais títulos na Netflix por tipo
types_by_Country = df.groupby(["country","type"])["show_id"].nunique().unstack().fillna(0)
types_by_Country["total"]= types_by_Country.sum(axis=1)
types_by_Country.sort_values(by="total", ascending=False).head(10).drop(columns="total").plot(
    kind="bar",
    title="Top 10 países com mais títulos na Netflix por tipo",
    color=["orange", "blue"],
)
plt.xlabel("País", fontsize=12, fontweight="bold")
plt.ylabel("Quantidade de títulos", fontsize=12, fontweight="bold")
plt.xticks(rotation=45, ha="right")
plt.legend(["Filmes", "Séries"], loc="upper right")
plt.tight_layout()
# plt.show()

#Visualização de crescimento da quantidade de titulos adicionados por pais
added_by_country_per_year = df.groupby(["country", "year_added"])["show_id"].nunique().unstack("year_added").fillna(0)
top10 = added_by_country_per_year.assign(total= added_by_country_per_year.sum(axis=1)).nlargest(10, "total").drop(columns="total")
top10.T.plot(
    kind="line",
    marker="o"
)
plt.xlabel("Ano", fontsize=12, fontweight="bold")
plt.ylabel("Total Adicionado", fontsize=12, fontweight= "bold")
plt.tight_layout()
plt.grid()
# plt.show()

#Classificação por genero de conteudo
titles_by_gender = df.groupby("listed_in")["show_id"].nunique().reset_index(name="count")
topGender = titles_by_gender.nlargest(10, "count")

topGender.plot(
    x="listed_in",
    y="count",
    title="Top gêneros de conteúdo",
    kind="bar",
    legend=False
)
plt.xlabel("Gênero", fontsize=12, fontweight="bold")
plt.ylabel("Quantidade de titulos", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.xticks(rotation=45, ha="right")
# plt.show()

#Grafico de preferencia por tipo de genero de conteudo 
gender_by_year = df.groupby(["listed_in", "year_added"])["show_id"].nunique().unstack().fillna(0).astype(int)
top10 = gender_by_year.assign(total=gender_by_year.sum(axis=1)).nlargest(10, "total")
top10.drop(columns="total", inplace=True)
top10.T.plot(
    kind="line",
    marker="o",
    title="Quantidade de conteudo adicionado por gênero"
)
plt.xlabel("Ano", fontsize=12, fontweight="bold")
plt.ylabel("Quantidade", fontsize=12, fontweight="bold")
plt.legend(loc="upper left")
plt.yticks(range(0, 800, 50))
plt.tight_layout()
plt.grid()
# plt.show()

#Ranking das combinações de gêneros no dataframe
combination_gender = df.groupby("title")["listed_in"].apply(list).reset_index(name="combination")
combination_gender["combination"] = combination_gender["combination"].apply(
    lambda x: list(combinations(x, 2))
)
all_combination = [comb for sublist in combination_gender["combination"] for comb in sublist]

cont_freq = Counter(all_combination)


dataFrameCombination = pandas.DataFrame(cont_freq.items(), columns=["gender", "count"]).sort_values(by="count", ascending=False)

dataFrameCombination.head(10).plot(
    x= "gender",
    y="count",
    title="Ranking de Combinações de Gênero",
    kind="bar"
)
plt.xlabel("Combinação", fontsize=12, fontweight= "bold")
plt.ylabel("Quantidade", fontsize=12, fontweight= "bold")
plt.tight_layout()
plt.show()


