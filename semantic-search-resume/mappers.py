def map_to_settings(args):

    database_config = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password,
        'schema_name': args.schema_name,
    }

    aws_config = {
        'key': args.aws_key,
        'secret': args.aws_secret,
        'region': args.aws_region
    }

    return {
        'database': database_config,
        'aws': aws_config
    }
