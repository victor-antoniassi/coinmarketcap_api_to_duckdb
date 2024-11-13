
# Script simples para consulta de cotações de criptomoedas utilizando a biblioteca dlt

Este repositório contém um script Python que demonstra o uso da biblioteca [dlt](https://github.com/dlt-hub/dlt), uma biblioteca para processos de extração e carregamento de dados.

## Sobre o Script

O script `dlt_to_duckdb.py` implementa um pipeline de dados EL (Extract, Load) que:

1. Extrai dados de preços e métricas de mercado das criptomoedas BTC, ETH e LTC da API da CoinMarketCap.
2. Transforma os dados em um formato estruturado.
3. Carrega os dados em um banco de dados DuckDB local.

Ele utiliza as seguintes bibliotecas Python:

- `dlt`: A biblioteca data load tool, que fornece abstrações para construir pipelines de dados.
- `duckdb`: O banco de dados DuckDB, utilizado como destino para os dados.
- `logging`: Para configurar um sistema de logs durante a execução do script.

## Pré-requisitos para execução do script

1. **Python 3.9+**
2. **Bibliotecas Python**: `dlt`, `logging`, `duckdb`
3. [Chave de API da CoinMarketCap](https://coinmarketcap.com/api/): Deve ser configurada no arquivo `secrets.toml` do DLT.

## Estrutura do Repositório
```
├── .dlt
│   └── secrets.toml
├── dlt_to_duckdb.py
└── requirements.txt
```
## Possíveis melhorias

- Explorar outras funcionalidades da biblioteca dlt, como o suporte a outras fontes de dados e destinos.
- Adicionar tratamento de erros e monitoramento mais avançado.
- Integrar o pipeline com o dbt e ferramentas de orquestração na nuvem.
