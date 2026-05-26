# Projeto — Tratamento de Dados Olist

## Descrição do Projeto

Este projeto realiza o tratamento e a sanitização de dois datasets da Olist utilizando Python e bibliotecas nativas.

O pipeline executa:
- leitura de arquivos CSV;
- tratamento de valores nulos;
- padronização textual;
- conversão de datas;
- validação de regras de negócio;
- exportação de arquivos tratados;
- geração de relatório estatístico manual.

O objetivo é preparar os dados para futuras análises ou aplicações de Machine Learning.

---

# Guia de Execução

1. Instale o Python.
2. Coloque os arquivos:
   - `olist_products_dataset.csv`
   - `olist_orders_dataset.csv`

   na pasta do projeto.

3. Execute o notebook:
```bash
main.ipynb
```
4. Ao final da execução serão gerados:
-`olist_products_dataset_tratado.csv`
-`olist_orders_dataset_tratado.csv`

O código não altera o arquivo original presente neste repositório.
