# Compressão de Imagens no AWS S3

## Descrição
Este script realiza a compressão de imagens armazenadas em um bucket da AWS S3. A partir de um arquivo CSV recebido como parâmetro, o script:
1. Faz o download das imagens do S3 para um diretório temporário.
2. Comprime as imagens (PNG, JPG, JPEG) com base em uma qualidade definida.
3. Faz o upload das imagens comprimidas de volta ao bucket S3, substituindo os arquivos originais.
4. Registra todas as ações em um arquivo de log para rastreabilidade.

## **Pré-requisitos**
Certifique-se de ter os seguintes requisitos instalados antes de executar o script:
- **Python 3.x**: Baixe e instale a versão mais recente do [Python](https://www.python.org/downloads/).
- **Bibliotecas necessárias**: Instale as dependências executando o seguinte comando:

```sh
pip install boto3 pillow dask
```

Além disso, é necessário que suas credenciais AWS estejam configuradas corretamente no ambiente para que o boto3 possa acessar o S3.

## **Parâmetros de Entrada**
O script aceita os seguintes argumentos:

| Parâmetro                  | Descrição                                                       | Padrão                     | Exemplo |
|-----------------------------|----------------------------------------------------------------|-----------------------------|---------|
| `--max_image_pixels`        | Número máximo de pixels permitidos por imagem               | `1000000000`                | `--max_image_pixels 500000000` |
| `--perc_compression_quality` | Qualidade da compressão da imagem (0 a 100)                   | `80`                         | `--perc_compression_quality 75` |
| `--temp_dir`                 | Diretório temporário para armazenar os arquivos baixados    | `Sistema operacional`        | `--temp_dir /tmp` |
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

## **Conclusão**
Este script é uma ferramenta eficiente para reduzir o tamanho de imagens armazenadas no S3, ajudando a economizar espaço e reduzir custos de armazenamento. Certifique-se de fornecer os argumentos corretamente e acompanhar os logs para monitorar o processamento.

