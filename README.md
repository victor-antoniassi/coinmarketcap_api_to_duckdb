# Consulta de cotações de criptomoedas utilizando a biblioteca dlt

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

## Pré-requisitos

1. **Python 3.9+**
2. **Bibliotecas Python**: `dlt`, `logging`, `duckdb`
3. [Chave de API da CoinMarketCap](https://coinmarketcap.com/api/): Deve ser configurada no arquivo `secrets.toml` do DLT.

## Instruções de Uso

1. Clone este repositório:

   ```bash
   git clone https://github.com/victor-antoniassi/coinmarketcap_api_to_duckdb.git
   cd coinmarketcap_api_to_duckdb
   ```

2. Crie e ative um ambiente virtual Python:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua chave de API da CoinMarketCap no arquivo e o local para criação do duckdb `secrets.toml` dentro da pasta `.dlt`:

5. Execute o script:

   ```bash
   python dlt_to_duckdb.py
   ```

   O script irá extrair os dados da API da CoinMarketCap, transformá-los e carregá-los em um banco de dados DuckDB local.

6. Após a execução, você pode consultar os dados carregados no banco DuckDB:

   ```python
   import duckdb

   with duckdb.connect("seu arquivo do duckdb .db") as db:
       db.sql("SELECT * FROM quotes_data.latest_quotes_data").show()
   ```

## Estrutura do Repositório

- `dlt_to_duckdb.py`: O script principal que implementa o pipeline de dados.
- `requirements.txt`: Lista das dependências Python necessárias.
- `secrets.toml`: Arquivo de configuração para armazenar a chave de API da CoinMarketCap.

## Próximos Passos

- Explorar outras funcionalidades da biblioteca dlt, como o suporte a outras fontes de dados e destinos.
- Adicionar tratamento de erros e monitoramento mais avançado.
- Integrar o pipeline com o dbt e ferramentas de orquestração na nuvem.
