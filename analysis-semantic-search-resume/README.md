# Analisador de logs do processo de busca semântica em currículos

## Descrição
Este script tem como finalidade processar arquivos de log gerados durante buscas semânticas em currículos, extraindo informações relevantes como schema, filtro, tipo de busca e tempo gasto, e armazenando os resultados em um arquivo CSV. O objetivo é facilitar a análise de desempenho e resultados das buscas realizadas.

O script percorre todos os arquivos `.log` de um diretório, extrai os dados de interesse e gera um relatório consolidado em formato CSV.

## Parâmetros
O script aceita os seguintes parâmetros:

| Parâmetro             | Tipo   | Descrição |
|---------------------- |--------|-----------|
| `--directory_logs`    | String | Diretório onde estão localizados os arquivos de log a serem processados. |
| `--report_file_path`  | String | Caminho do arquivo CSV onde os resultados serão armazenados. |

## Dependências
Para executar o script, as seguintes bibliotecas são necessárias:
- Python 3.x
- `os` (padrão na biblioteca do Python)
- `re` (padrão na biblioteca do Python)
- `csv` (padrão na biblioteca do Python)
- `argparse` (padrão na biblioteca do Python)

## Como executar com Docker
Para executar o script em um container Docker, siga os seguintes passos:

1. Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
CMD ["python", "analysis-semantic-search-resume-logs.py", "--directory_logs", "/logs", "--report_file_path", "/output/report.csv"]
```

2. Construa a imagem Docker:

```sh
docker build -t semantic-search-log-processor .
```

3. Execute o container:

```sh
docker run --rm -v $(pwd)/logs:/logs -v $(pwd)/output:/output semantic-search-log-processor
```

## Exemplo de Formato de Log
Um exemplo de entrada do arquivo de log processado pelo script:

```
2025-06-28 10:00:00,000 - INFO - [SCHEMA] - Processing records from: public
2025-06-28 10:00:01,000 - WARNING - Filter: Analista de Dados, Type: HNSW, Time Spent: 0.1234 seconds
```

## Exemplo de Saída do Arquivo CSV
Após o processamento do log, o arquivo CSV gerado terá um formato semelhante ao seguinte:

```
schema;filter_text;search_type;time_spent
public;Analista de Dados;HNSW;0.1234
```

## Referências
- [Script de Busca Semântica](https://github.com/DiovaniMotta/scripts-utils/tree/main/semantic-search-resume)
