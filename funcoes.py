import csv
import re



caminho_arquivo = "olist_products_dataset.csv"
def ler_csv(caminho_arquivo):

    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = []

        for linha in leitor:
            dados.append(linha)
        
    return dados


def tratar_nulos(dados):
    dados_nulos_tratados = dados
    contador_nulos_corrigidos = 0
    for linha in dados_nulos_tratados:
        if not linha["product_category_name"]:
            linha["product_category_name"] = "Sem Categoria"
            contador_nulos_corrigidos += 1
    return dados_nulos_tratados, contador_nulos_corrigidos



def padronizar_categorias(dados):
    dados_categorias_padronizadas = dados

    for linha in dados_categorias_padronizadas:
        categoria = linha["product_category_name"]
        categoria = categoria.strip()
        categoria = categoria.lower()
        categoria = re.sub(r'[^\w\s]', '', categoria)
        linha["product_category_name"] = categoria
    return dados_categorias_padronizadas


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

