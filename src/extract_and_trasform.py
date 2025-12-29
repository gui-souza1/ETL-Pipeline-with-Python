import requests
import pandas as pd
from datetime import datetime as dt, timezone
from zoneinfo import ZoneInfo

# Função para extrair dados da API
def extrair_dados_coinbase(TICKER:str)->dict:
    url = f'https://api.coinbase.com/v2/prices/{TICKER}-USD/spot'
    response = requests.get(url)
    return response.json()

# Função para cotação do dólar
def extrair_cotacao_usd_brl():
    api_key = "f1f6fd54d41540a3990dce5f72b806f1"  # Essa linha considera a variável definida no Job Databricks, valor original: dbutils.widgets.get("api_key")
    url = "https://api.currencyfreaks.com/v2.0/rates/latest"

    response = requests.get(url, params={"apikey": api_key})
    response.raise_for_status()

    data = response.json()

    try:
        return float(data["rates"]["BRL"])
    except KeyError as e:
        raise ValueError("Falha de resposta da API CurrencyFreaks") from e


# Transforma dados brutos da API: renomeia colunas e adiciona timestamp
def tratar_dados_criptomoedas(dados_criptomoedas:list, taxa_usd_brl:float)->dict:
    dados_tratados = []
    timestamp = dt.now(timezone.utc).astimezone(ZoneInfo("America/Sao_Paulo")).replace(microsecond=0, tzinfo=None)

    for cripto in dados_criptomoedas:  
        ticker = cripto['data']['base']
        valor_usd = float(cripto['data']['amount'])
        valor_brl = valor_usd * taxa_usd_brl
        moeda_original = cripto['data']['currency']
        
        dados_tratados.append({
            "ticker":ticker,
            "valor_usd": round(valor_usd,2),
            "valor_brl": round(valor_brl,2),
            "moeda_original":moeda_original,
            "taxa_conversao_usd_brl": round(taxa_usd_brl,2),
            "timestamp": timestamp
        })

    return dados_tratados

dados_bitcoin = extrair_dados_coinbase("BTC")
dados_ethereum = extrair_dados_coinbase("ETH")
dados_solana = extrair_dados_coinbase("SOL")

dados_criptomoedas = [dados_bitcoin, dados_ethereum, dados_solana]

taxa_usd_brl = extrair_cotacao_usd_brl()

dados_tratados = tratar_dados_criptomoedas(dados_criptomoedas, taxa_usd_brl)
print(dados_tratados)
