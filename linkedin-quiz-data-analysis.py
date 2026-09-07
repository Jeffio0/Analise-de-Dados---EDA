import os
import kagglehub
import matplotlib.pyplot as plt
import pandas as pd

# 1. Ingestão dos Dados via KaggleHub
path = kagglehub.dataset_download("kalilurrahman/linkedin-poll-data")
print("Path to dataset files:", path)

arquivos = os.listdir(path)
print("arquivos", arquivos)

caminho_completo = os.path.join(path, arquivos[0])
dados = pd.read_csv(caminho_completo)

# 2. Padronização das Colunas (PT-BR)
colunas_br = {
    'Quiz_number': 'num_quiz',
    'Total_Views': 'total_views',
    'Total_Responses': 'total_respostas',
    'Right_Answers': 'resp_corretas',
    'Total_Likes': 'total_curtidas',
    'Avg_right': 'media_acerto',
    'Max_Right': 'max_acerto',
}
dados.rename(columns=colunas_br, inplace=True)
dados.info()

# 3. Engenharia de Atributos (Métricas Percentuais)
# nova coluna engajamento % ((total_respostas/total_visualizações)*100)
dados['engajamento'] = (
    (dados['total_respostas'] / dados['total_views']) * 100
).round(2)

# nova coluna acertos % ((resp_corretas/total_respostas)*100)
dados['acertos'] = (
    (dados['resp_corretas'] / dados['total_respostas']) * 100
).round(2)

# 4. Análise por Respostas Corretas (Valores Absolutos)
maior_resp = dados[
    ['num_quiz', 'resp_corretas', 'acertos', 'dificuldade_3']
].sort_values(by='resp_corretas', ascending=False)
menor_resp = dados[
    ['num_quiz', 'resp_corretas', 'acertos', 'dificuldade_3']
].sort_values(by='resp_corretas', ascending=True)

display(maior_resp.head(1))
display(menor_resp.head(1))

# 5. Análise por Taxa de Acerto (%)
maior_taxa = dados[['num_quiz', 'acertos', 'dificuldade_3']].sort_values(
    by='acertos', ascending=False
)
menor_taxa = dados[['num_quiz', 'acertos', 'dificuldade_3']].sort_values(
    by='acertos', ascending=True
)

display(maior_taxa.head(1))
display(menor_taxa.head(1))

# 6. Filtro Condicional (.query)
# Quizzes com alta interatividade (>100 curtidas) e taxa de acertos > 60%
df_quiz = dados.query('total_curtidas > 100 & acertos > 60')
display(df_quiz.head())

# 7. Regra de Negócio: Categorização em 2 Níveis
dados['dificuldade'] = dados['acertos'].apply(
    lambda x: 'Difícil' if x < 60 else 'Fácil'
)


# 8. Regra de Negócio: Categorização em 3 Níveis
def categoria_dificuldade(acerto):
  if acerto >= 70:
    return 'Fácil'
  elif acerto >= 40:
    return 'Médio'
  else:
    return 'Difícil'


dados['dificuldade_3'] = dados['acertos'].apply(categoria_dificuldade)

# Contagem das questões por dificuldade
print(dados.groupby('dificuldade_3')['num_quiz'].count())

# 9. Visualização Gráfica (Distribuição Percentual)
plot_dificuldade = (
    dados['dificuldade_3'].value_counts(normalize=True) * 100
).round(2)

ax = plot_dificuldade.plot(
    kind='bar',
    figsize=(7, 7),
    color='blue',
    xlabel='Dificuldade do Quiz',
    ylabel='Percentual (%)',
    rot=0,
)

# Adiciona o percentual no topo de cada barra
ax.bar_label(ax.containers[0], fmt='%.2f%%', padding=3)
plt.title('Distribuição Percentual de Dificuldade dos Quizzes')
plt.ylim(0, plot_dificuldade.max() + 10)

plt.show()
