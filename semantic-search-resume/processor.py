import argparse
from vectors import BedrockClient
from database import Repository
from logger import info
from mappers import map_to_settings

def process(config):
    db_config = config.get('database')
    aws_config = config.get('aws')
    client = BedrockClient(aws_config)
    repository = Repository(db_config)

    terms = [
        # Vagas Copacol
        'Operador de Máquina - Fábrica de Farinha',
        'Estagiário SESMT',
        'Jovem Aprendiz Administrativo',
        'Operador de Máquina - Caldeira',
        'Zelador',
        'Motorista',
        'Líder de Operações Sala de Máquinas',
        'Trainee Analista de Processos e Custos',
        'Auxiliar de Operador de Máquinas - Climatização',
        'Operador de Climatização',
        'Auditor Interno',
        'Jovem Aprendiz Industrial',
        'Eletromecânico',
        'Operador de Máquina - Cereais',

        # Vagas Intelbras
        'Pessoa Analista de Suporte Técnico',
        'Pessoas com Deficiência (PCD)',
        'Estágio (Médio Técnico/Técnico/Superior/Tecnologia)',
        'Pessoa Analista Gestão de Pessoas Pl - Clima e Engajamento',
        'Pessoa Analista de Contabilidade Pl',
        'Pessoa Analista de Planejamento Integrado Pl',
        'Pessoa Assistente de Marketing',
        'Pessoa Estagiária Suporte Técnico - Energia',
        'Pessoa Estagiário (a) de Nível Superior ou Técnico - Suporte Técnico',
        'Técnico de Segurança do Trabalho Pl',
        'Pessoa Analista de Marketing Pl.',
        'Pessoa Estagiária Nível Superior - Importação',
        'Pessoa Estagiaria Nível Superior | Suporte Técnico',
        'Pessoa Analista Financeiro Jr. (Crédito e Cobrança)',
        'Pessoa Analista de Processos Industriais Sr - Filial Tubarão',
        'Técnico de Segurança do Trabalho',
        'Pessoa Estagiária Nivel Tecnologia - Câmeras Pug & Play',
        'Pessoa Técnica Segurança do Trabalho Jr',
        'Pessoa Estagiária Nivel Tecnologia - Desenvolvimento de Software',
        'Pessoa Analista de Negócios de TI Sr - Sistemas Corporativos',
        'Pessoa Desenvolvedora III - ABAP',
        'Pessoa Analista de Pricing Sr',
        'Pessoa Analista de Suporte Técnico Jr - Energia Solar',
        'Pessoa Supervisora de Produção - Montagem Cabos /Tubarão',
        'Pessoa Analista de SGI Pl - Filial Tubarão',
        'Pessoa Estagiária Nível Superior - Energia',
        'Pessoa Analista de Negócios de TI Sr - Sistemas Corporativos',
        'Montador',
        'Analista de Suporte Técnico Jr',
        'Pessoa Designer Gráfico Pl - Marketing Consumo',
        'Pessoa Estagiária Nivel Superior - Produtos e Negócios',
        'Pessoa Analista de Inteligência de Mercado Jr',
        'Pessoa Executiva de Vendas I - Distribuição Segurança Eletronica',
        'Pessoa Executiva de Vendas Sul - I - Distribuição Energia',
        'Pessoa Estagiária Nível Superior - Marketing',
        'Pessoa Gerente de Operações Logísticas',
        'Pessoa Analista Financeiro Sr - Crédito e Cobrança',
        'Pessoa Analista de Pós Vendas Jr',
        'Pessoa Auxiliar de Expedição',
        'Pessoa Designer UX/UI II - Cloud Services',
        'Pessoa Assistente Administrativo de Vendas',
        'Pessoa Analista de Pós Vendas Jr',
        'Pessoa Executiva de Vendas I - Distribuição Segurança Eletronica',
        'Pessoa Executiva de Vendas Sul - I - Distribuição Energia',
        'Pessoa Estagiaria Nível Superior | Comunicação em Nuvem',
        'Pessoa Executiva de Vendas N/NE/C.Oe I - Energia',

        #Vagas Senior Sistemas
        'Executivo(a) de Novos Negócios (Especialista ERP)',
        'Executivo(a) de Sucesso do Cliente',
        'Coordenador(a) de Faturamento',
        'Software Developer (Java/Spring)',
        'Product Analyst (Performance)',
        'Software Developer Java/Angular',
        'Executivo(a) de Novos Negócios (Construção)',
        'Software Developer FullStack (React/NodeJS)',
        'Software Architect .Net',
        'Executivo(a) Técnico(a) de Negócios (ERP)',
        'DevSecOps Infrastructure Analyst (Cloud)',
        'Analista de Cybersecurity',
        'Analista de Suporte (eSocial e Folha de Pagamento)',
        'Analista de Controles Internos (Compliance)',
        'Software Developer (TypeScript e React/ReactNative)',
        'Analista de Marketing',
        'Software Quality Analyst',
        'Coordenador(a) de Vendas'
    ]
    info('Starting search process...')
    for term in terms:
        info(f'Searching for {term} term.')
        info(f"Searching term sending vectorization: {term}.")
        embedding = client.generate_embedding(term)
        info(f'Searching term using HSNW index type')
        hnsw_records = repository.search_using_hnsw(term, embedding)
        index = 1
        for row in hnsw_records:
            info(f'{index}) Candidate: {row[0]} - {row[1]}')
            index = index + 1
        info('End search using HSNW index type\n')
        info(f'Searching term using IVFFlat index type')
        ivfflat_records = repository.search_using_ivfflat(term, embedding)
        index = 1
        for row in ivfflat_records:
            info(f'{index}) Candidate: {row[0]} - {row[1]}')
            index = index + 1
        info('End search using IVFFlat index type\n')
        info(f'Searching term using ts_vector')
        ts_vector_records = repository.search_using_ts_vector(term)
        index = 1
        for row in ts_vector_records:
            info(f'{index}) Candidate: {row[0]} - {row[1]}')
            index = index + 1
        info('End search using ts_vector\n')
    info(f"Process finished...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script settings configuration.")

    parser.add_argument(
        "-H", "--host",
        type=str,
        required=True,
        help="Host where the PostgreSQL server is running (e.g., localhost)"
    )
    parser.add_argument(
        "-P", "--port",
        type=int,
        default=5432,
        help="Port number for the PostgreSQL server (default: 5432)"
    )
    parser.add_argument(
        "-d", "--database",
        type=str,
        required=True,
        help="Name of the PostgreSQL database"
    )
    parser.add_argument(
        "-u", "--user",
        type=str,
        required=True,
        help="PostgreSQL database user"
    )
    parser.add_argument(
        "-p", "--password",
        type=str,
        required=True,
        help="Password for the PostgreSQL user"
    )
    parser.add_argument(
        "-s", "--schema_name",
        type=str,
        required=True,
        help="Name of the PostgreSQL schema to use"
    )
    parser.add_argument(
        "-k", "--aws_key",
        type=str,
        required=False,
        help="AWS access key ID"
    )
    parser.add_argument(
        "-a", "--aws_secret",
        type=str,
        required=False,
        help="AWS secret access key"
    )
    parser.add_argument(
        "-r", "--aws_region",
        type=str,
        default="sa-east-1",
        help="AWS region name (default: sa-east-1)"
    )

    args = parser.parse_args()
    settings = map_to_settings(args)

    process(settings)