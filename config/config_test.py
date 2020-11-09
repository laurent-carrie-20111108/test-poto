from project.config import Config


class TestConfig(Config):
    ENV_NAME = 'test'
    DEBUG = True
    TESTING = False

    MYSQL_DB = {
        'MYSQL_DATABASE_HOST': '104.154.34.14',
        'MYSQL_DATABASE_PORT': '3306',
        'MYSQL_DATABASE_USER': 'root',
        'MYSQL_DATABASE_PASSWORD': '8bogweFIIeEpuKED',
        'MYSQL_DATABASE_DB': 'test_20111108',
    }
