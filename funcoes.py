# Importando bibliotecas necessárias

import csv
import re
import datetime


# Função para ler o arquivo CSV e retornar os dados como uma lista de dicionários

caminho_arquivo = "olist_products_dataset.csv"
def ler_csv(caminho_arquivo):

    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = []

        for linha in leitor:
            dados.append(linha)
        
    return dados


# Função para tratar valores nulos na coluna "product_category_name" e contar quantos foram corrigidos

def tratar_nulos(dados):
    contador_nulos_corrigidos = 0

    for linha in dados:
        if not linha["product_category_name"]:
            linha["product_category_name"] = "Sem Categoria"
            contador_nulos_corrigidos += 1

    return dados, contador_nulos_corrigidos


# Função para padronizar os valores da coluna "product_category_name" (remover espaços, converter para minúsculas e remover caracteres especiais)
# Pode ser alterada para incluir outras colunas, caso necessário ao trocar o nome da coluna dentro da função ou criar uma lista de colunas a serem padronizadas e
# iterar sobre elas dentro da função, como foi feito para as dimensões físicas dos produtos.

def padronizar_categorias(dados):

    for linha in dados:
        categoria = linha["product_category_name"]
        categoria = categoria.strip()
        categoria = categoria.lower()
        categoria = re.sub(r'[^\w\s]', '', categoria)

        linha["product_category_name"] = categoria
    return dados


# Função para calcular a média de uma coluna numérica, ignorando valores nulos ou não numéricos

def calcular_media(dados, coluna):
    total = 0
    contador = 0

    for linha in dados:
        valor = linha.get(coluna)
        if valor is not None and valor.strip() != "":
            try:
                total += float(valor)
                contador += 1
            except ValueError:
                continue

    if contador > 0:
        return total / contador
    else:
        return None


# Função para tratar valores nulos nas colunas de dimensões físicas dos produtos, substituindo por médias calculadas e contando quantos foram corrigidos,
# A função salva as médias como float, caso necessário para padronização substituir a linha 95 por(linha[coluna] = str(medias_dimensoes.get(coluna, 0))
# o que vai manter todos os dados do dataset padronizados em string.

def tratar_dimensoes_nulas(dados):

    lista_dimensoes_fisicas = [
        "product_length_cm",
        "product_width_cm",
        "product_height_cm",
        "product_weight_g"
    ]
    medias_dimensoes = {}
    for coluna in lista_dimensoes_fisicas:
        media = calcular_media(dados, coluna)
        if media is not None:
            medias_dimensoes[coluna] = media
    linhas_nulos_corrigidos = 0
    for linha in dados:
        for coluna in lista_dimensoes_fisicas:
            valor = linha.get(coluna)
            if valor is None or str(valor).strip() == "":
                linha[coluna] = medias_dimensoes.get(coluna, 0)
                linhas_nulos_corrigidos += 1

    return dados, linhas_nulos_corrigidos


# Função para salvar os dados tratados em um novo arquivo CSV

def salvar_csv(dados, caminho_saida):
    if not dados:
        return
    colunas = dados[0].keys()
    with open(caminho_saida, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(
            arquivo,
            fieldnames=colunas
        )
        writer.writeheader()
        writer.writerows(dados)

# Função para converter as datas presentes no dataser "orders", 
# a função recebe os dados e o nome da coluna a ser convertida, e retorna a quantidade de datas convertidas.

def converter_data(dados, coluna):
    datas_convertidas = 0
    for linha in dados:
        data_str = linha.get(coluna)
        if data_str:
            try:
                data_obj = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
                linha[coluna] = data_obj.strftime("%d/%m/%Y")
                datas_convertidas += 1
            except ValueError:
                linha[coluna] = "nao especificada"
        else:
            linha[coluna] = "nao especificada"
    return datas_convertidas

# Função para conferir o status dos pedidos, verificando se há pedidos cancelados ou inconsistentes (sem data de entrega especificada e status diferente de "canceled")
# A função retorna a quantidade de pedidos cancelados e a quantidade de pedidos inconsistentes encontrados no dataset "orders".

def conferir_status_pedidos(dados):
    pedidos_cancelados = 0
    pedidos_inconsistentes = 0
    for linha in dados:
        data = linha.get("order_delivered_customer_date")
        status = linha.get("order_status")
        if data == "" or data == "nao especificada":
            if status == "canceled":
                pedidos_cancelados += 1
            else:
                pedidos_inconsistentes += 1

    return pedidos_cancelados, pedidos_inconsistentes


# Função para tratar colunas descritivas, substituindo valores nulos ou vazios por "0"(dados ausentes = "0") e contando quantos foram corrigidos.

def tratar_colunas_descritivas(dados):
    colunas = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty"
    ]

    contador = 0

    for linha in dados:
        for coluna in colunas:
            valor = linha.get(coluna)

            if valor is None or str(valor).strip() == "":
                linha[coluna] = "0"
                contador += 1

    return dados, contador