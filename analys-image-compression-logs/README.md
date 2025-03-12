# Log Processing Script

## Descrição
Este script tem como finalidade processar arquivos de log contendo informações sobre compressão de arquivos e armazenar os resultados em um arquivo CSV. Ele extrai dados relevantes, como tamanho original e comprimido dos arquivos, nome do bucket, caminho do arquivo CSV e ID do objeto processado.

O script analisa as informações logadas pela execução do [script de compressão de imagens](https://github.com/DiovaniMotta/scripts-utils/tree/main/image-compression), extraindo os dados necessários para gerar um relatório estruturado em CSV.

## Parâmetros
O script aceita os seguintes parâmetros:

| Parâmetro          | Tipo   | Descrição |
|---------------------|--------|------------|
| `--directory_logs` | String | Diretório onde estão localizados os arquivos de log a serem processados. |
| `--report_file_path` | String | Caminho do arquivo CSV onde os resultados serão armazenados. |

## Dependências
Para executar o script, as seguintes bibliotecas são necessárias:
- Python 3.x
- `re` (padrão na biblioteca do Python)
- `csv` (padrão na biblioteca do Python)
- `os` (padrão na biblioteca do Python)
- `argparse` (padrão na biblioteca do Python)

## Como executar com Docker
Para executar o script em um container Docker, siga os seguintes passos:

1. Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
CMD ["python", "script.py", "--directory_logs", "/logs", "--report_file_path", "/output/report.csv"]
```

2. Construa a imagem Docker:

```sh
docker build -t log-processor .
```

3. Execute o container:

```sh
docker run --rm -v $(pwd)/logs:/logs -v $(pwd)/output:/output log-processor
```

## Exemplo de Formato de Log
Um exemplo de entrada do arquivo de log processado pelo script:

```
2024-03-10 - Bucket Name: my-bucket
2024-03-10 - CSV Path: /data/file.csv
2024-03-10 Start processing object: obj_123
2024-03-10 File saved in /data/file.csv with size: 50.5 MB
2024-03-10 Upload object obj_123 with size: 25.2 MB
```

## Exemplo de Saída do Arquivo CSV
Após o processamento do log, o arquivo CSV gerado terá um formato semelhante ao seguinte:

```
execution_date;bucket_name;file;object;original_size_mb;compressed_size_mb;perc_compression
2024-03-10;my-bucket;/data/file.csv;obj_123;50.5;25.2;50.099
```

## Referências
- [Script de Compressão de Imagens](https://github.com/DiovaniMotta/scripts-utils/tree/main/image-compression)

