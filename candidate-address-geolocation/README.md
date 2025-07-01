# Geolocalização de Endereços de Candidatos

## Descrição
Este script tem como finalidade processar registros de endereços de candidatos armazenados em um banco de dados PostgreSQL, realizar consultas de geolocalização utilizando uma API (ex: HERE), e atualizar as coordenadas geográficas no banco. O processo é totalmente automatizado, com logs detalhados para cada etapa.

O script percorre todos os registros de endereço sem coordenadas, consulta a API de geolocalização, e atualiza o banco de dados com as coordenadas obtidas.

## Parâmetros
O script aceita os seguintes parâmetros:

| Parâmetro             | Tipo   | Descrição |
|---------------------- |--------|-----------|
| `--host`              | String | Host do banco de dados PostgreSQL |
| `--port`              | Int    | Porta do banco de dados (padrão: 5432) |
| `--database`          | String | Nome do banco de dados |
| `--user`              | String | Usuário do banco de dados |
| `--password`          | String | Senha do banco de dados |
| `--schema_name`       | String | Schema do banco de dados |
| `--geolocation_key`   | String | Chave de API da plataforma HERE (https://platform.here.com/portal/) |

## Dependências
Para executar o script, as seguintes bibliotecas são necessárias:
- Python 3.x
- `psycopg2`
- `argparse` (padrão na biblioteca do Python)
- `logging` (padrão na biblioteca do Python)

## Como executar com Docker
Para executar o script em um container Docker, siga os seguintes passos:

1. Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
CMD ["python", "processor.py", "--host", "<host>", "--port", "<port>", "--database", "<db>", "--user", "<user>", "--password", "<pwd>", "--schema_name", "<schema>", "--geolocation_key", "<api_key>"]
```

2. Construa a imagem Docker:

```sh
docker build -t candidate-address-geolocation .
```

3. Execute o container:

```sh
docker run --rm -v $(pwd)/logs:/logs candidate-address-geolocation
```

## Exemplo de Log Gerado
Um exemplo de entrada do arquivo de log processado pelo script:

```
2025-07-01 16:17:17,622 - INFO - Geolocation founded: POINT(-48.06897 -15.87282)
2025-07-01 16:17:17,643 - INFO - Update 492862f5-d1ab-4544-9618-961a31d1fdae record completed
2025-07-01 16:17:17,643 - ERROR - an error occurred while processing the geolocation query for addresses: 'NoneType' object has no attribute 'replace'
```

## Referências
- [Documentação HERE Geocoding & Search API](https://developer.here.com/documentation/geocoding-search-api/dev_guide/index.html)
- [Documentação psycopg2](https://www.psycopg.org/docs/)
