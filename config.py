import configparser

def main():
    conf = configparser.ConfigParser()
    conf.read('config')
    print(conf["Database"]['Path'])

main()
