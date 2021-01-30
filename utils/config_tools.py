import fileinput
import configparser as conf
import sys

DEFAULT_CONFIG_FILE = 'default.conf'
CONFIG_FILE = 'config.conf'


def replace_ini_file(file, search_exp, replace_exp):
    for line in fileinput.input(file, inplace=1):
        if search_exp in line:
            line = line.replace(line, search_exp + ' = ' + replace_exp + '\n')
        sys.stdout.write(line)


def change_to_default(file_default=DEFAULT_CONFIG_FILE, file_conf=CONFIG_FILE):
    default = conf.ConfigParser()
    default.read(file_default)
    with open(file_conf, 'w') as configfile:
        default.write(configfile)

def get_sections():
    config = conf.ConfigParser()
    config.read(CONFIG_FILE)
    return config.sections()


def get_params(section):
    config = conf.ConfigParser()
    config.read(CONFIG_FILE)
    return config.items(section)


def get_config(section, parameter):
    config = conf.ConfigParser()
    config.read(CONFIG_FILE)
    return config[section][parameter]


def set_config(section, parameter, value):
    config = conf.ConfigParser()
    config.read(CONFIG_FILE)
    config[section][parameter] = value
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)