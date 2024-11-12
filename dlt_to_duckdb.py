"""
Script para extrair dados de criptomoedas da CoinMarketCap API e carregar em um banco DuckDB.

Este script implementa um pipeline de dados ETL (Extract, Transform, Load) que:
1. Extrai dados de preços e métricas de mercado das criptomoedas BTC, ETH e LTC
2. Transforma os dados em um formato estruturado
3. Carrega os dados em um banco de dados DuckDB local

Requisitos:
    - Python 3.9+
    - Bibliotecas: dlt, logging, duckdb
    - Chave de API da CoinMarketCap (deve ser configurada em .dlt/secrets.toml)

Autor: Victor Antoniassi
Data: Novembro 2024
"""

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.auth import APIKeyAuth
import logging
import duckdb

# Configuração do sistema de logs para monitoramento e debugging
# Definimos o nível como INFO para ver informações importantes durante a execução
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dlt.resource(name="latest_quotes_data")
def extract_and_load():
    """
    Função principal que extrai dados da API da CoinMarketCap e prepara para carregamento.
    
    Esta função:
    1. Autentica com a API usando uma chave armazenada de forma segura
    2. Faz uma requisição para obter dados das criptomoedas BTC, ETH e LTC
    3. Processa a resposta e extrai métricas relevantes
    4. Gera registros formatados para serem carregados no banco de dados
    
    Yields:
        dict: Dicionário contendo as métricas de cada criptomoeda com as seguintes chaves:
            - symbol: Símbolo da criptomoeda (ex: BTC)
            - price: Preço atual em USD
            - volume_24h: Volume de negociação nas últimas 24 horas
            - market_cap: Capitalização de mercado
            - last_updated: Data/hora da última atualização
    """
    # Obtém a chave de API do arquivo de secrets do dlt
    api_key = dlt.secrets["coinmarketcap.api_key"]
    
    # Configura a autenticação com a API usando APIKeyAuth
    auth = APIKeyAuth(
        name="X-CMC_PRO_API_KEY",  # Nome do header de autenticação requerido pela API
        api_key=api_key,           # Chave de API obtida do arquivo de secrets
        location="header"          # Localização onde a chave deve ser enviada
    )
    
    # Inicializa o cliente REST com a URL base da API e configurações de autenticação
    client = RESTClient(
        base_url="https://pro-api.coinmarketcap.com/v1",
        auth=auth
    )

    # Faz a requisição HTTP GET para obter os dados mais recentes
    # Especificamos as criptomoedas desejadas e a moeda de conversão (USD)
    response = client.get(
        "/cryptocurrency/quotes/latest",
        params={
            "symbol": "BTC,ETH,LTC",  # Símbolos das criptomoedas que queremos dados
            "convert": "USD"           # Moeda para conversão dos valores
        }
    )
    
    # Verifica se a requisição foi bem-sucedida
    # Um código 200 indica sucesso na resposta HTTP
    if response.status_code != 200:
        logger.error(
            "Erro na chamada da API. Status: %s, Detalhes: %s",
            response.status_code,
            response.text
        )
        response.raise_for_status()

    # Processa cada criptomoeda retornada pela API
    for coin_data in response.json()["data"].values():
        # Extrai dados específicos do USD do objeto de cotações
        quote = coin_data.get("quote", {}).get("USD", {})
        
        # Cria um dicionário com os dados que queremos armazenar
        data = {
            "symbol": coin_data.get("symbol"),      # Símbolo da criptomoeda
            "price": quote.get("price"),            # Preço atual
            "volume_24h": quote.get("volume_24h"),  # Volume de negociação 24h
            "market_cap": quote.get("market_cap"),  # Capitalização de mercado
            "last_updated": quote.get("last_updated")  # Timestamp da atualização
        }
        
        # Verifica se temos dados válidos antes de yield
        # Isso evita carregar registros vazios no banco de dados
        if any(data.values()):
            yield data
        else:
            logger.warning(
                "Registro vazio ignorado para: %s",
                coin_data.get("symbol")
            )

def run_pipeline():
    """
    Configura e executa o pipeline de dados.
    
    Esta função:
    1. Cria um novo pipeline dlt configurado para usar DuckDB
    2. Executa o pipeline com nossa função de extração
    3. Registra informações sobre o carregamento dos dados
    
    O banco de dados será criado no arquivo 'crypto_quotes.db' no diretório atual.
    """
    # Configura o pipeline especificando nome, destino e dataset
    pipeline = dlt.pipeline(
        pipeline_name="crypto_quotes_pipeline",  # Nome único do pipeline
        destination=dlt.destinations.duckdb(dlt.secrets["destination.duckdb_path"]),  # Banco DuckDB
        dataset_name="quotes_data"  # Nome do schema do banco
    )

    # Executa o pipeline e captura informações sobre o carregamento
    load_info = pipeline.run(extract_and_load)
    logger.info("Informações de carregamento do pipeline: %s", load_info)

def query_data():
    """
    Função para consultar os dados carregados no banco de dados DuckDB.
    """
    with duckdb.connect(dlt.secrets["destination.duckdb_path"]) as db:
        # Executa a consulta SQL e exibe os resultados
        db.sql("SELECT * FROM quotes_data.latest_quotes_data").show()
  
# Ponto de entrada do script        
if __name__ == "__main__":
    run_pipeline(),
    query_data()