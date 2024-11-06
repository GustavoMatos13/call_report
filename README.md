
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API REST - Chamadas Telefônicas</title>
</head>
<body>

    <h1>API REST - Chamadas Telefônicas</h1>

    <p>Este projeto tem como objetivo receber informações de duração de uma chamada, para calcular as taxas, sendo elas fixas e/ou por minuto de acordo com as especificações de horário. O projeto recebe os dados e armazena em dois detalhamentos da chamada: o início e o fim, enviando como parâmetro para os cadastros dos registros, o número de telefone de origem e o número de telefone destino.</p>

    <hr>

    <h2>Instalação do Projeto</h2>

    <h3>Passos para rodar o projeto:</h3>

    <ol>
        <li><strong>Clonar o repositório</strong>: Clone o projeto para sua máquina local utilizando o comando abaixo:
            <pre><code>git clone https://github.com/GustavoMatos13/call_report.git</code></pre>
        </li>

        <li><strong>Criar e ativar o ambiente virtual</strong>: Crie um ambiente virtual com o comando:
            <pre><code>python -m venv venv</code></pre>
            <strong>Ativar o ambiente virtual:</strong>
            <ul>
                <li>No <strong>Windows</strong>: <pre><code>.\venv\Scripts\activate</code></pre></li>
            </ul>
        </li>

        <li><strong>Instalar as dependências do projeto</strong>: Com o ambiente virtual ativado, instale as dependências utilizando:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>

        <li><strong>Rodar as migrações do banco de dados</strong>: Aplique as migrações necessárias para configurar o banco de dados:
            <pre><code>python manage.py migrate</code></pre>
        </li>

        <li><strong>(Opcional) Criar um superusuário para o admin do Django</strong>: Caso queira acessar a interface administrativa do Django, crie um superusuário:
            <pre><code>python manage.py createsuperuser</code></pre>
        </li>
    </ol>

    <hr>

    <h2>Testes</h2>

    <p>Para testar a API, você pode cadastrar um novo registro de chamada através da URL:</p>

    <p><strong>POST:</strong><br>
    <code>http://127.0.0.1:8000/api/call/post</code></p>

    <h3>Parâmetros para cadastro de uma chamada (Exemplo):</h3>
    <pre><code>{
  "call_id": "01",
  "start": "2016-02-29T12:00:00Z",
  "end": "2016-02-29T14:00:00Z",
  "source": "11913210118",
  "destination": "1125136526"
}</code></pre>

    <p>Para obter os resultados de um registro, acesse a URL abaixo, substituindo <strong>{CALL_ID}</strong> pelo ID da chamada:</p>

    <p><strong>GET:</strong><br>
    <code>http://127.0.0.1:8000/api/call/get/{CALL_ID}</code></p>

    <hr>

    <h2>Descrição do Ambiente de Trabalho</h2>

    <ul>
        <li><strong>Sistema Operacional</strong>: Windows</li>
        <li><strong>IDLE</strong>: Visual Studio Code</li>
    </ul>

    <h3>Bibliotecas e Frameworks usados no projeto:</h3>

    <ul>
        <li>asgiref==3.8.1</li>
        <li>Django==5.1.2</li>
        <li>django-cors-headers==4.6.0</li>
        <li>djangorestframework==3.15.2</li>
        <li>flake8==7.1.1</li>
        <li>gunicorn==23.0.0</li>
        <li>inflection==0.5.1</li>
        <li>mccabe==0.7.0</li>
        <li>packaging==24.1</li>
        <li>psycopg2==2.9.10</li>
        <li>pycodestyle==2.12.1</li>
        <li>pyflakes==3.2.0</li>
        <li>pytz==2024.2</li>
        <li>PyYAML==6.0.2</li>
        <li>sqlparse==0.5.1</li>
        <li>tzdata==2024.2</li>
        <li>uritemplate==4.1.1</li>
    </ul>

</body>
</html>
