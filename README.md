# assesment-2xt

Este repositório contém uma aplicação desenvolvida para um teste técnico, descrito em: http://stub.2xt.com.br/pCuwoCxInvjSutnq9Dp7WpKaqrHqOzvw

# Tecnologias utilizadas
## Armazenamento: 
* Postgresql - https://www.postgresql.org/
## Aplicação e CLI: 
* Python 3.7 - https://www.python.org/
* Flask - https://palletsprojects.com/p/flask/
* Click - https://palletsprojects.com/p/click/
* Psycopg2 - http://initd.org/psycopg/docs/
* Requests - https://2.python-requests.org//en/master/

## Provisionamento: 
* NGINX - https://www.nginx.com/
* UWSGI - https://uwsgi-docs.readthedocs.io/en/latest/
* Docker - https://www.docker.com/
* Docker Compose - https://docs.docker.com/compose/

# Como rodar esse projeto localmente
## Requisitos: 
* Sitema operacional baseado em Unix
* Git - https://git-scm.com/downloads
* Docker - https://www.docker.com/products/docker-desktop
* Docker Compose - https://docs.docker.com/compose/install/

## Passos a passo: 
1 - Clonar o repositório
```bash
git clone https://github.com/jfredericon/assesment-2xt.git && cd assesment-2xt
```
2 - Dentro da pasta Flask renomeie o arquivo .env-example para .env e adicione os valores para as variaveis de ambiente  
**ATENÇÃO**: É importante que os variáveis relacionadas com o banco possuam os mesmos valores para ***"PORTA"***, ***"USUARIO"***, ***"SENHA"***, ***"NOME DO BANCO"*** que os especificados no arquivo ***docker-compose.yml*** na raiz do projeto; e o valor do ***"HOST"*** deve ser ***"127.0.0.1"***  para o anquivo ***".env"*** e ***"postgres"*** para o arquivo ***docker-compose.yml***  
  
3 - Subir o container com a aplicação: 
```bash
make
```
4 - Entrar no container da aplicação para execução dos comandos na CLI para geração da base de dados, criação das tabelas e busca e processamto dos dados na api
```bash
make cli
```
5 - Crie a base de dados e as tabelas
```bash
python manage.py migrate
```
6 - Busque e processe os dados da API
```bash
python manage.py data-only
```
7 - A aplicação estará acessivel no endereço 
```bash
http://localhost
```

### OBS:
Você pode verificar os demais comandos na CLI e que ação ele realiza utilizando o comando
```bash
python manage.py --help
```
Você pode parar a execução da aplicação executando o comando
```bash
make stop
```
Você pode parar a execução da busca e processamento dos dados pressionando ***CTRL + C***
    
Você pode sair do container da aplicação após os passos da CLI executando o comando
```bash
exit
```

Juntamente com a aplicação é servido um container rodando o ***PGADMIN4*** que pode ser acessado em ***http://localhost:16543***  
e as credenciais podem ser verificadas no arquivo ***docker-compose.yml*** na raiz do projeto

