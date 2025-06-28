def map_to_settings(args):
    database = {
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    }

    directories = {
        'input': args.directory_logs,
        'output': args.directory_output
    }

    return {
        'database': database,
        'directories': directories
    }