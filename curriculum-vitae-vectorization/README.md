# Resume Vector POC

## Visão Geral

Este projeto tem como objetivo consultar currículos de candidatos salvos em uma base de dados e submetê-los à vetorização utilizando o Amazon Bedrock. A solução permite realizar buscas vetoriais, facilitando a identificação de currículos mais relevantes para determinada consulta.

## O que são buscas vetoriais?

Buscas vetoriais são técnicas de recuperação de informações que utilizam representações numéricas (vetores) de textos, imagens ou outros dados. Ao invés de comparar palavras-chave, as buscas vetoriais comparam a similaridade entre vetores, permitindo encontrar resultados semanticamente semelhantes, mesmo que não utilizem exatamente os mesmos termos.

## Funcionalidade

- Consulta currículos de candidatos armazenados em uma base de dados.
- Submete os currículos à vetorização utilizando o Amazon Bedrock.
- Permite buscas vetoriais para encontrar currículos mais relevantes de acordo com a consulta realizada.
- Gera logs detalhados do processamento.

## Requisitos de Software e Bibliotecas

- Python 3.12 ou superior
- Bibliotecas Python necessárias (instale via pip):
  - boto3
  - pandas
  - numpy
  - pymysql
  - python-dotenv
  - tqdm

Você pode instalar as dependências com:

```powershell
pip install boto3 pandas numpy pymysql python-dotenv tqdm
```

## Parâmetros e Configurações Necessárias

- **Banco de Dados:**
  - Configure as credenciais e a string de conexão do banco de dados no arquivo `.env` ou diretamente no código (`database_functions.py`).
- **Amazon Bedrock:**
  - Configure as credenciais AWS (chave de acesso e segredo) no ambiente ou via arquivo de configuração padrão da AWS.
- **Logs:**
  - Os logs são gerados no diretório `logs/`.
- **Outros parâmetros:**
  - Parâmetros de vetorização e busca podem ser ajustados nos arquivos `vectors.py` e `processor.py`.

## Parâmetros de Entrada do Script

| Parâmetro (CLI)   | Nome Interno       | Tipo | Obrigatório | Valor Padrão | Descrição                                                                                  |
|-------------------|--------------------|------|--------------|---------------|--------------------------------------------------------------------------------------------|
| `-H`, `--host`    | `host`             | str  | Sim          | -             | Host do servidor PostgreSQL                                                                |
| `-P`, `--port`    | `port`             | int  | Não          | 5432          | Porta do servidor PostgreSQL                                                               |
| `-d`, `--database`| `database`         | str  | Sim          | -             | Nome do banco de dados PostgreSQL                                                          |
| `-u`, `--user`    | `user`             | str  | Sim          | -             | Usuário do banco de dados PostgreSQL                                                       |
| `-p`, `--password`| `password`         | str  | Sim          | -             | Senha do usuário do banco de dados                                                         |
| `-s`, `--schema_name` | `schema_name`  | str  | Sim          | -             | Nome do schema do PostgreSQL                                                               |
| `-t`, `--type_integration` | `type_integration` | int  | Não          | 1             | Tipo de integração: `1` = ALL_CANDIDATES, `2` = ONLY_NOT_PROCESSED_YET (padrão: 1)        |
| `-k`, `--aws_key` | `aws_key`          | str  | Não          | -             | AWS Access Key ID                                                                          |
| `-a`, `--aws_secret` | `aws_secret`    | str  | Não          | -             | AWS Secret Access Key                                                                      |
| `-r`, `--aws_region` | `aws_region`    | str  | Não          | sa-east-1     | Região AWS (padrão: sa-east-1)                                                             |


## Execução

1. Configure as variáveis de ambiente necessárias (banco de dados e AWS).
2. Execute o script principal conforme a documentação interna dos arquivos Python.

---

Para mais detalhes sobre o funcionamento interno, consulte os arquivos `vectors.py`, `processor.py` e `database_functions.py`.
