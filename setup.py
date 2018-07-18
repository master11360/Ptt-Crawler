def execute(cmd):
    from subprocess import call
    call(cmd.split(' '))


execute('pip install -U scrapy')
execute('pip install -U beautifulsoup4')
execute('pip install -U sqlalchemy')
