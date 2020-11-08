import logging

from werkzeug.utils import import_string


class Config(object):
    DEBUG = False
    TESTING = False


def load_config(app, config_module):
    try:
        cfg = import_string(config_module)()
        app.config.from_object(cfg)
        logging.info('Config {} loaded.'.format(app.config['ENV_NAME']))
        return True
    except ImportError:
        logging.debug('Cannot load {}'.format(config_module))
        return False


def load_config_prod(app):
    return load_config(app, 'config.config_prod.ProdConfig')


def load_config_stage(app):
    return load_config(app, 'config.config_stage.StageConfig')


def load_config_dev(app):
    return load_config(app, 'config.config_dev.DevConfig')


def load_config_test(app):
    return load_config(app, 'config.config_test.TestConfig')


def load_all_configs(app):
    load_config_functions = [load_config_prod,
                             load_config_stage,
                             load_config_dev]
    for load_config_fct in load_config_functions:
        if load_config_fct(app):
            return
