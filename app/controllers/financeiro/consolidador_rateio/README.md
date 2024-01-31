# Consolidador de Rateio
---
## Objetivo
* Consolidar os arquivos de rateio em um unico arquivo.

## Dependencias Adicionais
* Pandas
* Xlrd
* Openpyxl

## Github
* https://github.com/CovabraCIC/cic-portal/tree/master/app/controllers/financeiro/consolidador_rateio

## Origem Dados
* Arquivos de rateio em excel fornecidos pelos usuarios.

## Resumo da Execucao
1) O usuario **seleciona os arquivos** de rateio que deseja consolidar.
2) Ler os arquivos e **contatenam** as informacoes em um **unico DataFrame**.
3) Cria uma **copia** do DataFrame contatenado **removendo as linhas duplicadas** usando a chave "**Codigo Barras**" e "**Loja**".
4) Atualiza o **Valor** no Dataframe copia com a **soma dos valores** agrupados por **Codigo Barras** e **Loja**.
5) **Salva** o DataFrame copia em um **novo arquivo**.
6) Disponibiliza um **link** para **download** do arquivo consolidado.