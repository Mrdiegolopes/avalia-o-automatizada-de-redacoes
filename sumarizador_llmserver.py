# ex: reuse your existing OpenAI setup
from openai import OpenAI
import time
import os

start_time = time.time()

pasta_atual = os.path.dirname(__file__)

# caminho para o arquivo dentro da subpasta 'dados'
caminho_arquivo = os.path.join(pasta_atual, 'dados', 'documento_a_ser_sumarizado.txt')

with open(caminho_arquivo, 'r') as arquivo:
    conteudo = arquivo.read()

qtd_palavras = 400

# point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

system_message = f"""
Você é um assitente que tem como objetivo de criar um resumo a partir de um texto longo. O resumo produzido por você deve atender os três critérios a seguir:
    1) O resumo deve capturar os pontos principais e as ideias centrais do texto, mantendo a precisão e o contexto original, sem adicionar informações não presentes no texto longo;
    2) O resumo deve ser conciso, com apenas um parágrafo e ter, no máximo, {qtd_palavras} palavras. Em hipótese alguma exceda o limite de {qtd_palavras} palavras;
    3) Na resposta ao usuário, deve ser retornado apenas o texto do resumo produzido. Você não pode, em hipótese alguma, escrever textos cumprimentando o usuário ou adicionando quaisquer blocos de textos antes ou depois do resumo produzido.
"""
user_message = f"""
    Faça o resumo do seguinte texto longo:
    "{conteudo}"
"""

completion = client.chat.completions.create(
  model="gemma-3-12b-it",
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
  ],
  temperature=0.7,
)

print(completion.choices[0].message.content)

end_time = time.time()
duration = end_time - start_time
print(f"tempo de execução: {duration} segundos.")
print(f"total de tokens prompt: {completion.usage.prompt_tokens} tokens.")
print(f"total de tokens da saida: {completion.usage.completion_tokens} tokens.")