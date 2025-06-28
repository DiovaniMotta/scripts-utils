# Extrator de Detalhes de Currículos

## Descrição
Este script tem como finalidade processar arquivos de log e extrair conteúdos de currículos armazenados em um banco de dados PostgreSQL, agrupando e salvando os resultados em arquivos de texto estruturados. Ele permite organizar os conteúdos por filtros e tipos de busca, facilitando análises posteriores.

O script conecta-se ao banco de dados, lê os conteúdos dos currículos de candidatos, agrupa os resultados e os salva em arquivos de saída, conforme os parâmetros fornecidos.

## Parâmetros
O script aceita os seguintes parâmetros:

| Parâmetro              | Tipo   | Descrição |
|------------------------|--------|-----------|
| `--host`               | String | Host do banco de dados PostgreSQL |
| `--port`               | String | Porta do banco de dados |
| `--database`           | String | Nome do banco de dados |
| `--user`               | String | Usuário do banco de dados |
| `--password`           | String | Senha do banco de dados |
| `--directory_logs`     | String | Diretório onde estão localizados os arquivos de log a serem processados. |
| `--directory_output`   | String | Diretório onde os arquivos de saída serão armazenados. |

## Dependências
Para executar o script, as seguintes bibliotecas são necessárias:
- Python 3.x
- `psycopg2`
- `os` (padrão na biblioteca do Python)
- `re` (padrão na biblioteca do Python)
- `argparse` (padrão na biblioteca do Python)
- `collections` (padrão na biblioteca do Python)

## Como executar com Docker
Para executar o script em um container Docker, siga os seguintes passos:

1. Crie um `Dockerfile` com o seguinte conteúdo:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
CMD ["python", "extract-details-resume-logs.py", "--host", "<host>", "--port", "<port>", "--database", "<db>", "--user", "<user>", "--password", "<pwd>", "--directory_logs", "/logs", "--directory_output", "/output"]
```

2. Construa a imagem Docker:

```sh
docker build -t extract-details-resume .
```

3. Execute o container:

```sh
docker run --rm -v $(pwd)/logs:/logs -v $(pwd)/output:/output extract-details-resume
```

## Exemplo de Formato de Log
Um exemplo de entrada de log ou parâmetro processado pelo script:

```
12345, filtro: Analista de Dados, tipo: busca_simples
67890, filtro: Engenheiro de Software, tipo: busca_avancada
```

## Exemplo de Saída dos Arquivos
Após o processamento, os arquivos de saída terão um formato semelhante ao seguinte:

```
#term = Analista de Dados

# busca_simples

1) Conteúdo do currículo do candidato 12345

# busca_avancada

1) Conteúdo do currículo do candidato 67890
```

## Referências
- [Documentação psycopg2](https://www.psycopg.org/docs/)
