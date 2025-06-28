# Analisador de Busca Semântica em Currículos

## Descrição
Este módulo realiza buscas semânticas em currículos utilizando embeddings de texto e banco de dados PostgreSQL com suporte a vetores (HNSW). Ele permite a integração com AWS Bedrock para geração de embeddings e armazena logs detalhados do processo.

O sistema é composto por scripts que conectam-se ao banco de dados, geram embeddings para termos de busca, executam consultas vetoriais e registram logs do processamento.

## Parâmetros
Os scripts aceitam os seguintes parâmetros (via argparse):

| Parâmetro         | Tipo   | Descrição |
|-------------------|--------|-----------|
| `--host`          | String | Host do banco de dados PostgreSQL |
| `--port`          | String | Porta do banco de dados |
| `--database`      | String | Nome do banco de dados |
| `--user`          | String | Usuário do banco de dados |
| `--password`      | String | Senha do banco de dados |
| `--schema_name`   | String | Schema do banco de dados |
| `--aws_key`       | String | Chave de acesso AWS (opcional) |
| `--aws_secret`    | String | Segredo de acesso AWS (opcional) |
| `--aws_region`    | String | Região AWS (opcional, padrão: sa-east-1) |

## Dependências
Para executar o módulo, as seguintes bibliotecas são necessárias:
- Python 3.x
- `psycopg2`
- `boto3`
- `json` (padrão)
- `logging` (padrão)
- `os` (padrão)
- `argparse` (padrão)

## Exemplo de Uso
```sh
python processor.py --host <host> --port <port> --database <db> --user <user> --password <pwd> --schema_name <schema> --aws_key <key> --aws_secret <secret> --aws_region <region>
```

## Exemplo de Log Gerado
```
2025-06-28 10:00:00,000 - INFO - [SCHEMA] - Processing records from: public
2025-06-28 10:00:01,000 - WARNING - Filter: Operador de Máquina, Type: HNSW, Time Spent: 0.1234 seconds
```

## Exemplo de Consulta SQL Utilizada
```
SELECT ca.id, ca."name" 
FROM <schema>.candidate ca 
JOIN <schema>.candidate_resume_vector_hnswm crv 
ON crv.candidate = ca.id            
WHERE crv.embedding <=> %s::vector < 1.0
ORDER BY crv.embedding <=> %s::vector 
LIMIT 100;
```

## Referências
- [Documentação AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [Documentação PostgreSQL Vetores](https://github.com/pgvector/pgvector)
