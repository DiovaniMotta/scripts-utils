# Compressão de Imagens no AWS S3

## Descrição
Este script realiza a compressão de imagens armazenadas em um bucket da AWS S3. A partir de um arquivo CSV recebido como parâmetro, o script:
1. Faz o download das imagens do S3 para um diretório temporário.
2. Comprime as imagens (PNG, JPG, JPEG, MPO) com base em uma qualidade definida.
3. Faz o upload das imagens comprimidas de volta ao bucket S3, substituindo os arquivos originais.
4. Registra todas as ações em um arquivo de log para rastreabilidade.

## **Pré-requisitos**
Certifique-se de ter os seguintes requisitos instalados antes de executar o script:
- **Python 3.12.3**: Baixe e instale a versão mais recente do [Python](https://www.python.org/downloads/).
- **Bibliotecas necessárias**: Instale as dependências executando o seguinte comando:

```sh
pip install boto3 pillow dask opencv-python
```

Além disso, é necessário que suas credenciais AWS estejam configuradas corretamente no ambiente para que o boto3 possa acessar o S3.


É possível executar o script através de uma imagem docker. A seguir estão contidos os passos para configuração:

### **Instruções de Configuração do Ambiente com Docker**

- **Docker**: Certifique-se de ter o Docker instalado em seu sistema. Caso não tenha, você pode baixar e instalar o Docker [aqui](https://www.docker.com/get-started).

1. **Criação do Dockerfile**

   Crie um arquivo chamado `Dockerfile` no mesmo diretório do seu script com o seguinte conteúdo:

   ```Dockerfile
   # Use uma imagem base com Python 3
   FROM python:3.12.3-slim

   # Defina o diretório de trabalho
   WORKDIR /app

   # Copie os arquivos do script e o arquivo CSV para o container
   COPY . /app

   # Instale as dependências necessárias
   RUN pip install boto3 pillow dask opencv-python

   # Exponha a porta 80, caso necessário
   EXPOSE 80

   # Comando para rodar o script
   CMD ["python", "compress_images_from_S3.py"]
   ```

2. **Construção da Imagem Docker**

   No terminal, navegue até o diretório onde o `Dockerfile` está localizado e execute o comando abaixo para construir a imagem Docker:

   ```sh
   docker build -t compress-images-s3 .
   ```

3. **Execução do Container**

   Após a imagem ser construída, você pode rodar o container usando o comando abaixo. Lembre-se de fornecer os parâmetros necessários para a execução do script, como o nome do bucket S3 e o caminho para o arquivo CSV.

   ```sh
   docker run -v /local/path/to/csv:/app/dataset.csv compress-images-s3 --bucket_name meu-bucket --csv_path /app/dataset.csv
   ```

   **Notas:**
   - Substitua `/local/path/to/csv` pelo caminho real onde o arquivo CSV está localizado em seu sistema local.
   - O comando `-v /local/path/to/csv:/app/dataset.csv` monta o arquivo CSV no container, permitindo que o script o acesse.

## **Parâmetros de Entrada**
O script aceita os seguintes argumentos:

| Parâmetro                  | Descrição                                                       | Padrão                     | Exemplo |
|-----------------------------|----------------------------------------------------------------|-----------------------------|---------|
| `--max_image_pixels`        | Número máximo de pixels permitidos por imagem               | `1000000000`                | `--max_image_pixels 500000000` |
| `--perc_compression_quality` | Qualidade da compressão da imagem (0 a 100)                   | `80`                         | `--perc_compression_quality 75` |
| `--temp_dir`                 | Diretório temporário para armazenar os arquivos baixados    | `Sistema operacional`        | `--temp_dir /tmp` |
 `--ignore_trunc`             | Indica se erros de truncamento (arquivos corrompidos) devem ser ignorados. Se `True`, o script continua mesmo com arquivos corrompidos. | `True` | `--ignore_trunc False` |
| `--bucket_name`              | Nome do bucket S3 onde as imagens estão armazenadas           | **Obrigatório**            | `--bucket_name meu-bucket` |
| `--csv_path`                 | Caminho para o arquivo CSV contendo as chaves das imagens     | **Obrigatório**            | `--csv_path /caminho/para/dataset.csv` |

### **Exemplo de Execução**
```sh
python compress_images_from_S3.py --bucket_name meu-bucket --csv_path /caminho/para/dataset.csv
```

## **Formato do Arquivo CSV**
O script requer um arquivo CSV contendo os caminhos das imagens armazenadas no S3. O formato esperado é:

```csv
path
imagens/imagem1.jpg
imagens/imagem2.png
imagens/imagem3.jpeg
```
Cada linha deve conter o caminho relativo do objeto dentro do bucket.

## **Rastreabilidade**
Todas as operações realizadas pelo script são registradas em um arquivo de log gerado automaticamente com timestamp no nome. O log contém informações sobre:
- Início e fim do processamento
- Arquivos baixados do S3
- Compressão realizada e tamanho final
- Upload do arquivo comprimido para o S3
- Exclusão do arquivo temporário
- Possíveis erros encontrados

Exemplo de log gerado:
```log
2024-02-01 12:00:00 - INFO - Downloading object imagens/imagem1.jpg from AWS S3.
2024-02-01 12:00:05 - INFO - File saved in /tmp/imagem1.jpg with size: 3.5 MB
2024-02-01 12:00:10 - INFO - Compressing /tmp/imagem1.jpg object as JPEG file
2024-02-01 12:00:15 - INFO - Upload object imagens/imagem1.jpg for bucket meu-bucket with size 2.1 MB
2024-02-01 12:00:20 - INFO - File /tmp/imagem1.jpg was deleted.
```

## **Avisos**
Durante a execução do script, os seguintes avisos podem ser registrados nos logs:

| **Código**              | **Descrição**                                                                                                                                         |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[CORRUPT_FILE]**          | A imagem está corrompida e não pôde ser lida corretamente. Ela será ignorada.                                                                         |
| **[INVALID_EXTENSION]**     | O formato da imagem não é suportado para compressão (como BMP ou TIFF, por exemplo). Esse arquivo será ignorado.                                       |
| **[INVALID_CONTENT]**       | Falha ao tentar fazer upload de uma imagem com conteúdo vazio, o que pode indicar que a compressão falhou.                                            |
| **[FILE_DELETED]**          | O arquivo foi removido do bucket S3 antes de ser processado.                                                                                         |
| **[TRUNCATED_IMAGE]**       | A imagem estava truncada, mas, dependendo da configuração, o erro pode ser ignorado ou registrado.                                                    | 

## **Conclusão**
Este script é uma ferramenta eficiente para reduzir o tamanho de imagens armazenadas no S3, ajudando a economizar espaço e reduzir custos de armazenamento. Certifique-se de fornecer os argumentos corretamente e acompanhar os logs para monitorar o processamento.

