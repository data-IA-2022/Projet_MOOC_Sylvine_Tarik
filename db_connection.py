import yaml
from sqlalchemy import create_engine
from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder

def connect_to_db(config_file, section, ssh=False, local_port=None, ssh_section=None):

    # Read configuration information from file
    config = yaml.safe_load(open(config_file, 'r'))

    if local_port:
        config[section]['port'] = local_port

    if ssh:
        ssh_config = config[ssh_section]
        server = SSHTunnelForwarder(
            ssh_address_or_host=(ssh_config['host'], ssh_config['port']),
            ssh_username=ssh_config['user'],
            ssh_password=ssh_config['password'],
            remote_bind_address=(config[section]['host'], config[section]['port'])
        )
        server.start()

        if config[section]['type'] == 'mongodb':
            url = 'mongodb://127.0.0.1:{}/'.format(server.local_bind_port)

            client = MongoClient(url)

            return client[config[section]['db_name']]

        url = '{type}://{user}:{password}@127.0.0.1:{port}/{db_name}'.format(**config[section])

        engine = create_engine(url)

        return engine.connect()

    else:
        if config[section]['type'] == 'mongodb':
            url = 'mongodb://{host}:{port}/'.format(**config[section])

            client = MongoClient(url)

            return client[config[section]['db_name']]

        url = '{type}://{user}:{password}@{host}:{port}/{db_name}'.format(**config[section])
        print(url)

        engine = create_engine(url)

        return engine.connect()