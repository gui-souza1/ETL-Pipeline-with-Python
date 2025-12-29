# Código para ser executado no ambiente Databricks!!

df_pandas = pd.DataFrame(dados_tratados)

# Salvando dados em formato JSON usando Pandas (Databricks Volume)
event_ts = dados_tratados[0]["timestamp"]
ts = event_ts.strftime("%Y%m%d_%H%M%S_%f")
json_file = f"/Volumes/pipeline_api_coinbase/lakehouse/json_criptomoedas_coinbase/BTC_ETH_SOL_{ts}.json"
df_pandas.to_json(json_file, orient='records', date_format='iso',indent=2)
print(f"Arquivo JSON salvo:{json_file}")

# Adicionando registros na tabela usando Spark
df_spark = spark.createDataFrame(df_pandas)
# df_spark.printSchema()
df_spark.write.format('delta').mode('append').saveAsTable('pipeline_api_coinbase.cripto_data.cripto_data')