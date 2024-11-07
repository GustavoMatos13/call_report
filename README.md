# API REST CHAMADAS TELEFÔNICAS

Este projeto tem como objetivo receber informações de duração de uma chamada,
para calcular as taxas, sendo elas fixa e/ou por minuto de acordo com as especificações de
horário, este projeto recebe os dados e armazena em dois detalhamentos da chamada, o
início e fim, enviando como parâmetro para os cadastros dos registros, o número de
telefone de origem e o número de telefone destino.

## INSTALAÇÃO DO PROJETO:

- sera necessario clonar o projeto do repositorio
    https://github.com/GustavoMatos13/call_report.git
- criar uma venv com o comando: “python -m venv venv”
- ativá-lo “.\venv\Scripts\activate” (windows)
- instale as dependências do projeto com o comando “pip install -r requirements.txt”
- rode as migrações do banco com os comandos “python manage.py migrate”
- (opcional) para configurar o ADMIN crie um super usuário
    “python manage.py createsuperuser”
- ajustar o arquivo de settings.py para o banco local do sqlite  

 DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.sqlite3',  
        'NAME': BASE_DIR / 'db.sqlite3',  
     }  
 }  

## TESTES:
para testar você pode cadastrar um novo registro de chamada através da url:
.../api/call/post

os parâmetros são (exemplo):

{  
"call_id": "01",  
"start": "2016-02-29T12:00:00Z",  
"end": "2016-02-29T14:00:00Z",  
"source": "11913210118",  
"destination": "1125136526"  
}  

para obter os resultados você acessa:
.../api/call/get/{CALL_ID}

## DESCRIÇÃO DE AMBIENTE DE TRABALHO:
- Sistema Operacional: WINDOWS
- IDLE: Visual Studio Code
- Deploy: fly io
- Biblioteca e Framework usados no projeto:
- asgiref==3.8.1
- Django==5.1.2
- django-cors-headers==4.6.0
- djangorestframework==3.15.2
- flake8==7.1.1
- gunicorn==23.0.0
- inflection==0.5.1
- mccabe==0.7.0
- packaging==24.1
- psycopg2==2.9.10
- pycodestyle==2.12.1
- pyflakes==3.2.0
- pytz==2024.2
- PyYAML==6.0.2
- sqlparse==0.5.1
- tzdata==2024.2
- uritemplate==4.1.1


# DOCUMENTAÇÃO API 

## cadastrar o registro:  
https://telefonica.fly.dev/api/call/post  
call_id:77,start:2018-02-28T21:57:13Z,end:2018-03-01T22:10:56Z,source:99988526423,destination:9933468278

#### Enviar como string sem espaços e nessa formatação, pois é uma limitação do fly io


- call_id- Tem que ser único, usado para identificação de cada par de registro
- start- data de início da chamada
- end- data com a finalização da chamada
- source- telefone de origem pode conter apenas 10 ou 11 dígitios com o código de área
- destination- telefone destino pode conter apenas 10 ou 11 dígitios com o código de área

## obter registro(s):  
https://telefonica.fly.dev/api/call/{SOURCE}/{MONTH}/{YEAR}

- source- parâmetro obrigatório, telefone de origem
- month- opcional, mês de referência de registro
- year- opcional, ano de referência de registro
