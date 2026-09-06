import os
import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("kalilurrahman/linkedin-poll-data")

print("Path to dataset files:", path)

arquivos = os.listdir(path)
print("arquivos", arquivos)

caminho_completo = os.path.join(path, arquivos[0])
dados = pd.read_csv(caminho_completo)
dados.head()

# rename das colunas de pt-br -> ing direto no dataframe
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
# tipo de dados das colunas
dados.info()

# nova coluna engajamento % ((total_respostas/total_visualizações)*100)
dados['engajamento'] = (
    (dados['total_respostas'] / dados['total_views']) * 100
).round(2)
# nova coluna acertos % ((resp_corretas/total_respostas)*100)
dados['acertos'] = (
    (dados['resp_corretas'] / dados['total_respostas']) * 100
).round(2)
dados.head().sort_values(by='acertos', ascending=False)

# organizando listando o quiz com maior acerto e menor acerto
maior_acerto = dados[['num_quiz', 'resp_corretas']].sort_values(
    by='resp_corretas', ascending=False
)
menor_acerto = dados[['num_quiz', 'resp_corretas']].sort_values(
    by='resp_corretas', ascending=True
)
# visualizando somente o maior e menor valor
display(maior_acerto.head(1))
display(menor_acerto.head(1))

# criação de consulta para quiz > 100 curtidas, acerto > 50%
df_quiz = dados.query('total_curtidas > 100 & acertos > 50')
df_quiz.head()

# Coluna condicional para nível de dificuldade aplicando o lambda para dois níveis de dificuldade
dados['dificuldade'] = dados['acertos'].apply(
    lambda x: 'Difícil' if x < 60 else 'Fácil'
)
dados.head()


# função para três níveis de dificuldade
def categoria_dificuldade(acerto):
  if acerto >= 70:
    return 'Fácil'
  elif acerto >= 40:
    return 'Médio'
  else:
    return 'Difícil'


# Criação da nova coluna com 3 dificuldades
dados['dificuldade_3'] = dados['acertos'].apply(categoria_dificuldade)
dados.head()

# Contagem das questões por dificuldade
dados.groupby('dificuldade_3')['num_quiz'].count()