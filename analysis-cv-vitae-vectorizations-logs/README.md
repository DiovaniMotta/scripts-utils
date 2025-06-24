# Análise de Logs de Vetorização de Currículos

Este script tem como objetivo analisar arquivos de log gerados durante o processamento de vetorização de currículos (CVs), extraindo informações relevantes sobre o número de tokens processados para cada candidato e gerando um relatório consolidado em formato CSV.

## Objetivo
O script percorre um diretório contendo arquivos de log (`.log`), identifica para cada candidato o número de tokens processados (informação presente nas linhas de log), e salva um relatório CSV com o identificador do candidato e a respectiva contagem de tokens.

## Parâmetros de Configuração
O script deve ser executado via linha de comando e aceita os seguintes parâmetros obrigatórios:

- `-d` ou `--directory_logs`: Caminho para o diretório onde estão localizados os arquivos de log a serem processados.
- `-r` ou `--report_file_path`: Caminho para o arquivo CSV de saída, onde será salvo o relatório consolidado.

### Exemplo de uso
```bash
python analys-curriculum-vitae-vectorization-logs.py -d ./logs -r ./relatorio.csv
```

## Pré-requisitos
- **Python 3.6 ou superior**
- Não são necessárias bibliotecas externas além das já incluídas na biblioteca padrão do Python (`os`, `re`, `csv`, `argparse`).

## Funcionamento
1. O script percorre todos os arquivos `.log` no diretório especificado.
2. Para cada arquivo, identifica os candidatos processados e extrai o número de tokens de cada um.
3. Gera (ou atualiza) um arquivo CSV com duas colunas: `candidate` (ID do candidato) e `tokens` (quantidade de tokens processados).

## Observações
- O script pode ser executado em sistemas Windows, Linux ou MacOS.
- O arquivo CSV será criado caso não exista, ou atualizado caso já exista.

---

**Autor:** Diovani Motta
**Data:** Junho/2025
