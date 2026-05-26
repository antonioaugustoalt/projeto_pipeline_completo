import csv
import re
import datetime



caminho_arquivo = "olist_products_dataset.csv"
def ler_csv(caminho_arquivo):

    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = []

        for linha in leitor:
            dados.append(linha)
        
    return dados


def tratar_nulos(dados):
    contador_nulos_corrigidos = 0

    for linha in dados:
        if not linha["product_category_name"]:
            linha["product_category_name"] = "Sem Categoria"
            contador_nulos_corrigidos += 1

    return dados, contador_nulos_corrigidos



def padronizar_categorias(dados):

    for linha in dados:
        categoria = linha["product_category_name"]
        categoria = categoria.strip()
        categoria = categoria.lower()
        categoria = re.sub(r'[^\w\s]', '', categoria)

        linha["product_category_name"] = categoria
    return dados


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
    return datas_convertidas


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
