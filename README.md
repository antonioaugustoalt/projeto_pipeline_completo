# Projeto — Tratamento de Dados Olist

## Descrição do Projeto

A Olist identificou inconsistências em seus datasets de produtos e pedidos,
como valores nulos, datas inválidas e informações textuais despadronizadas. 
Esses problemas dificultam análises estatísticas e futuras aplicações de Machine Learning.

O objetivo deste projeto foi desenvolver um pipeline de tratamento de dados utilizando Python e bibliotecas nativas para realizar:
- leitura de arquivos CSV;
- tratamento de valores nulos;
- padronização textual;
- conversão de datas;
- validação de regras de negócio;
- exportação de arquivos tratados;
- geração de relatório manual.

Ao final do processamento, os datasets são exportados já sanitizados para novos arquivos CSV.

---

# Guia de Execução

1. Instale o Python em sua máquina.

2. Coloque os arquivos:
- `olist_products_dataset.csv`
- `olist_orders_dataset.csv`

na pasta do projeto.

3. Execute o notebook:

```bash
main.ipynb
```

4. Após a execução serão gerados:
- `olist_products_dataset_tratado.csv`
- `olist_orders_dataset_tratado.csv`

---

5. Conclusão sobre hipótese de negócio

  A diretoria identificou que muitas datas de entrega (order_delivered_customer_date) estão vazias.
a hipótese de negócio da Olist: essas datas estão nulas obrigatoriamente porque o status do pedido (order_status) consta como cancelado (canceled)

  Entretanto, foi possível identificar diversos pedidos que não foram cancelados e não possuem data (data nula/vazia). Com isso, a hipótese se prova falsa.

# Reflexão Teórica sobre Machine Learning

Dados que não forem devidamente selecionados e tratados não podem gerar um bom aprendizado para qualquer modelo de machine learning,
pois eles farão com que o modelo aprenda apenas ruidos e detalhes específicos do dataset ao invés de padrões realmente uteis.

Por isso, uma boa lógica de programação, voltada para a sanitização desses dados, é suficiente para garantir dados mais precisos
e uteis e confiaveis para o modelo, facilitando futuras analises e treinamento de Inteligência Artificial

