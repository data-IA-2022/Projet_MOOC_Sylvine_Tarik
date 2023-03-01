import yaml
import paramiko
import subprocess
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from pymongo import MongoClient


def demande_bool(text: str, value_True: list, value_False: list) -> bool:

    while True:

        a = input(text)

        if a.strip() in value_True:
            return True

        if a.strip() in value_False:
            return False


def create_db(config_file, section, ssh=False, local_port=None, ssh_section=None, pyodbc = False):

    # Read configuration information from file
    config = yaml.safe_load(open(config_file, 'r'))

    params = ''

    if pyodbc:
        config[section]['type'] += '+pyodbc'
        params = '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

    if ssh:
        ssh_config = config[ssh_section]['user']
        
        # Connect to database using SSH tunnel
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_config['host'], ssh_config['port'], ssh_config['user'], ssh_config['password'])
    
        if local_port:
            config[section]['port'] = local_port

    if config[section]['type'] == 'mongodb':
        url = 'mongodb://{host}:{port}/'.format(**config[section])

        client = MongoClient(url)

        return client[config[section]['db_name']]

    db_name = config[section]['db_name']
    num = 2

    while True:

        url = '{type}://{user}:{password}@{host}:{port}/{dbn}{params}'.format(**config[section], dbn = db_name, params= params)

        if database_exists(url):

            db_name = config[section]['db_name'] + str(num)
            num += 1

            continue
        break

    if num > 2:
        print(f"\nLa base de donnée '{config[section]['db_name']}' existe déjà.")

        if not demande_bool(f"-> Enregistrer sous le nom '{db_name}' (y/n) ? ", ['y', 'Y', 'yes', 'o', 'O', 'oui'], ['n', 'N', 'no', 'non']):

            return None

    # Connect to database using SQLAlchemy

    if pyodbc:
        engine = create_engine(url, fast_executemany=True)

    else:
        engine = create_engine(url)

    create_database(url, 'utf8mb4')

    return engine


def connect_to_db(config_file, section, ssh=False, local_port=None, ssh_section=None):

    # Read configuration information from file
    config = yaml.safe_load(open(config_file, 'r'))

    
        


    if local_port:
        config[section]['port'] = local_port

    # Connect to database using SQLAlchemy
    if config[section]['type'] == 'mongodb':
        url = 'mongodb://{host}:{port}/'.format(**config[section])

        client = MongoClient(url)

        return client[config[section]['db_name']]

    url = '{type}://{user}:{password}@{host}:{port}/{db_name}'.format(**config[section])

    engine = create_engine(url)
    
    return engine.connect()