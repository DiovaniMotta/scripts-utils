# Rotina de Manutenção e Reindexação de Índices no Elasticsearch

## Descrição
Este script automatiza a manutenção de índices em clusters Elasticsearch, permitindo operações de deleção, reindexação, backup e restauração de índices. Ele foi desenvolvido para facilitar a gestão de índices, otimizando o uso de recursos e garantindo a integridade dos dados durante processos de manutenção.

O script pode operar em diferentes modos, realizando desde a exclusão de índices vazios até a reindexação completa de índices com backup automático. Todas as operações são registradas em logs detalhados para rastreabilidade.


## Modos de Operação
O script suporta os seguintes modos de operação, definidos pelo parâmetro `--mode`:

| Modo      | Descrição |
|-----------|-----------|
| `ALL`     | Executa a exclusão de índices sem documentos e reindexa os índices com documentos. É o modo mais completo, realizando todas as etapas de manutenção. |
| `DELETE`  | Apenas exclui índices que não possuem documentos (índices "vazios"). Não realiza reindexação ou backup. |
| `REINDEX` | Apenas reindexa índices que possuem documentos, realizando backup, exclusão e recriação dos índices. Não exclui índices vazios. |
| `ONLY`    | Executa operações apenas nos índices especificados em um arquivo CSV fornecido pelo usuário. Ideal para manutenção seletiva. |
| `SEARCH`  | Lista e exibe informações detalhadas sobre os índices que correspondem ao prefixo informado, sem realizar alterações. Útil para auditoria e diagnóstico. |

### Detalhamento das Operações

#### ALL
- Busca todos os índices que correspondem ao prefixo informado.
- Exclui índices sem documentos.
- Para índices com documentos:
  - Cria um índice de backup (`backup-<index_name>`).
  - Replica os documentos do índice original para o backup.
  - Exclui o índice original.
  - Recria o índice original com os parâmetros informados.
  - Replica os documentos do backup para o índice recriado.

#### DELETE
- Busca todos os índices que correspondem ao prefixo informado.
- Exclui apenas os índices que não possuem documentos.

#### REINDEX
- Busca todos os índices que correspondem ao prefixo informado.
- Para cada índice com documentos:
  - Cria um índice de backup (`backup-<index_name>`).
  - Replica os documentos do índice original para o backup.
    - **A reindexação é executada de forma assíncrona. O script dispara a tarefa de reindexação e, a cada 5 segundos, consulta automaticamente o status da tarefa no Elasticsearch até a conclusão.**
  - Exclui o índice original.
  - Recria o índice original com os parâmetros informados.
  - Replica os documentos do backup para o índice recriado.
    - **A reindexação do backup para o índice recriado também é feita de forma assíncrona, com consulta do status a cada 5 segundos.**

#### ONLY
- Lê um arquivo CSV contendo os nomes dos índices a serem processados.
- Executa as operações de manutenção apenas nos índices listados no arquivo.

##### Exemplo de arquivo CSV para o modo ONLY:

```csv
index_name
hcm-rs-ana-carolinacombr
hcm-rs-grsdesacopladocombr
hcm-rs-diovanimottacombr
```

#### SEARCH
- Busca e lista todos os índices que correspondem ao prefixo informado.
- Exibe informações detalhadas como nome, número de shards, réplicas, quantidade de documentos e uso de memória de cada índice.
- Não realiza nenhuma alteração nos índices, apenas consulta e apresenta os dados.

##### Exemplo de uso do modo SEARCH:

```sh
python runner.py --host http://localhost:9200 --mode SEARCH --prefix hcm-rs-*
```

Saída esperada (exemplo):

```
Index: hcm-rs-ana-carolinacombr | Shards: 1 | Réplicas: 1 | Docs: 10000 | Memória: 50.2MB
Index: hcm-rs-grsdesacopladocombr | Shards: 1 | Réplicas: 1 | Docs: 5000 | Memória: 20.1MB
...
```

## Operações Realizadas no Elasticsearch

Abaixo estão exemplos das chamadas de API realizadas pelo script:

- **Buscar índices:**
  ```http
  GET <host>/<prefix>/_stats?level=shards
  ```
- **Buscar configurações dos índices:**
  ```http
  GET <host>/<prefix>/_settings
  ```
- **Criar índice:**
  ```http
  PUT <host>/<index_name>
  {
    "settings": {
      "number_of_shards": <shards>,
      "number_of_replicas": <replicas>
    }
  }
  ```
- **Reindexar documentos (assíncrono):**
  ```http
  POST <host>/_reindex?wait_for_completion=false
  {
    "source": { "index": "<index_name_origin>" },
    "dest": { "index": "<index_name_destination>" }
  }
  ```
  - O Elasticsearch retorna um campo `task` que identifica a tarefa de reindexação.
  - O script consulta o status da tarefa a cada 5 segundos até a conclusão:
    ```http
    GET <host>/_tasks/<task_id>
    ```
- **Excluir índice:**
  ```http
  DELETE <host>/<index_name>
  ```


## Pré-requisitos
Certifique-se de ter os seguintes requisitos instalados antes de executar o script:
- **Python 3.7.16** ou superior
- **Bibliotecas necessárias:**

```sh
pip install requests dask
```

## Configuração do Ambiente com Docker

- **Docker:** Certifique-se de ter o Docker instalado em seu sistema. Caso não tenha, você pode baixar e instalar o Docker [aqui](https://www.docker.com/get-started).

1. **Criação do Dockerfile**

   Crie um arquivo chamado `Dockerfile` no mesmo diretório do seu script com o seguinte conteúdo:

   ```Dockerfile
  FROM python:3.7.16-slim
   WORKDIR /app
   COPY . /app
   RUN pip install requests dask
   CMD ["python", "runner.py"]
   ```

2. **Construção da Imagem Docker**

   No terminal, navegue até o diretório onde o `Dockerfile` está localizado e execute:

   ```sh
   docker build -t reindex-elasticsearch .
   ```

3. **Execução do Container**

   Após a imagem ser construída, rode o container usando:

   ```sh
   docker run -v /local/path/to/csv:/app/indices.csv reindex-elasticsearch --host http://localhost:9200 --mode ONLY --file /app/indices.csv
   ```
   - Substitua `/local/path/to/csv` pelo caminho real do arquivo CSV em seu sistema local.
   - O parâmetro `--file` é obrigatório apenas no modo `ONLY`.


## Exemplo de Execução

```sh
python runner.py --host http://localhost:9200 --mode ALL --shards 1 --replicas 1 --prefix hcm-rs-*
```

Exemplo para o modo ONLY, utilizando um arquivo CSV:

```sh
python runner.py --host http://localhost:9200 --mode ONLY --file ./indices.csv
```

## Parâmetros de Entrada

| Parâmetro      | Abreviação | Descrição                                                                 | Padrão         | Exemplo | Obrigatório |
|--------------- |-----------|--------------------------------------------------------------------------|--------------- |---------|-------------|
| `--host`       | `-H`      | Endereço do cluster Elasticsearch                                         | -              | `--host http://localhost:9200` | Verdadeiro |
| `--mode`       | `-m`      | Modo de operação: ALL, DELETE, REINDEX, ONLY, SEARCH                             | `ALL`          | `--mode REINDEX` | Falso |
| `--shards`     | `-s`      | Número de shards para criação de novos índices                           | `1`            | `--shards 3` | Falso |
| `--replicas`   | `-r`      | Número de réplicas para criação de novos índices                         | `1`            | `--replicas 2` | Falso |
| `--prefix`     | `-p`      | Prefixo dos índices a serem processados                                 | `hcm-rs-*`     | `--prefix hcm-rs-*` | Falso |
| `--file`       | `-f`      | Caminho para o arquivo CSV com índices (obrigatório no modo ONLY)        | -              | `--file /app/indices.csv` | Falso* |

*Obrigatório apenas se o modo selecionado for `ONLY`.

## Rastreabilidade e Logs

Todas as operações realizadas pelo script são registradas em arquivos de log gerados automaticamente com timestamp no nome, localizados no diretório `logs/`. Os logs incluem:
- Início e fim do processamento
- Parâmetros utilizados
- Índices encontrados, excluídos, reindexados ou recriados
- Resultados das chamadas de API
- Possíveis erros encontrados

Exemplo de log gerado:
```log
2025-08-21 07:24:06 - INFO - Start the Elasticsearch cluster maintenance process...
2025-08-21 07:24:06 - INFO - Parameters:
2025-08-21 07:24:06 - INFO -    Cluster host: http://localhost:9200
2025-08-21 07:24:06 - INFO -    Operation mode: ALL
2025-08-21 07:24:06 - INFO -    Number of shards: 1
2025-08-21 07:24:06 - INFO -    Number of replicas: 1
2025-08-21 07:24:06 - INFO -    Prefix of the analyzed indices: hcm-rs-*
2025-08-21 07:24:06 - INFO - Found 2 indices with no documents
2025-08-21 07:24:06 - INFO - Starting deletion for index: 'hcm-rs-ana-carolinacombr'
2025-08-21 07:24:06 - INFO - Has the index deletion process been completed? True
2025-08-21 07:24:06 - INFO - Finishing the deletion process for indices without documents.
```

## Conclusão
Este script é uma ferramenta robusta para manutenção de índices em clusters Elasticsearch, proporcionando automação, segurança e rastreabilidade em operações críticas. Certifique-se de fornecer os argumentos corretamente e acompanhe os logs para monitorar o processamento.
