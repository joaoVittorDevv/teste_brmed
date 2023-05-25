[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Django](https://img.shields.io/badge/framework-Django-092E20.svg?logo=django)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/framework-DRF-092E20.svg?logo=django)](https://www.django-rest-framework.org/)
[![Redis](https://img.shields.io/badge/database-Redis-DC382D.svg?logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg?logo=postgresql)](https://www.postgresql.org/)
[![Celery](https://img.shields.io/badge/task%20queue-Celery-37814A.svg?logo=celery)](https://docs.celeryproject.org/)
[![MailHog](https://img.shields.io/badge/email%20testing-MailHog-00BACD.svg?logo=mailhog)](https://github.com/mailhog/MailHog)

# Teste BR Med

Teste prático de programação para a empresa BR Med

## Tecnologias utilizadas no projeto

Este projeto utiliza várias tecnologias-chave:

- **Django**: Um framework de alto nível para Python que permite um rápido desenvolvimento de aplicações.
- **Django Rest Framework**: Um kit de ferramentas poderoso e flexível para a construção de APIs na Web.
- **Postgres**: Um sistema de gerenciamento de banco de dados relacional de código aberto poderoso, que tem uma forte reputação por sua confiabilidade, integridade de dados e precisão.
- **Celery**: Um sistema de fila de tarefas assíncronas distribuídas que se concentra em processamento de dados em tempo real, enquanto também suporta agendamento de tarefas.
- **Redis**: Um armazenamento de dados na memória, usado como banco de dados, cache e corretor de mensagens.
- **Mailhog**: Uma ferramenta de teste de e-mail para desenvolvedores.


## Pré-requisitos

Antes de começar, certifique-se de que você tenha o Docker instalado em sua máquina. Caso não tenha, siga as instruções abaixo para instalá-lo.

### Instalação do Docker

## Instalação do Docker

Para instalar o Docker, siga estas etapas:

1. Baixe e instale o Docker de acordo com o seu sistema operacional. Você pode encontrar os instaladores no [site oficial do Docker](https://www.docker.com/products/docker-desktop).

2. Verifique se o Docker foi instalado corretamente executando o seguinte comando no terminal:

   ```bash
   docker --version


### Docker Compose

Certifique-se de ter o Docker Compose instalado em sua máquina. Você pode encontrar as instruções de instalação adequadas para o seu sistema operacional no [site oficial do Docker Compose](https://docs.docker.com/compose/install/).

*Lembre-se de verificar as instruções específicas para o seu sistema operacional antes de instalar o Docker Compose.*


## Como usar

Para subir o projeto utilizando o Docker Compose, siga as instruções abaixo:

1. Clone este repositório em sua máquina local.
2. Navegue até o diretório do projeto.
3. Execute o seguinte comando:

    ```bash
    docker-compose up --build 
    ```

Na primeira execução do projeto, você poderá enfrentar um tempo de espera mais longo por dois motivos principais: o Docker estará realizando o build de todas as dependências e também ocorrerá a primeira solicitação à API para registrar as cotações dos últimos trinta dias.

Caso não seja a primeira vez que você está executando o projeto, você pode utilizar o seguinte comando:

    
    docker-compose up
    

Se tudo estiver configurado corretamente, seu aplicativo agora deve estar disponível em `0.0.0.0:8000`.

Além da tela principal, também foi configurada uma tarefa no Celery para verificar se existem novos dados na API de cotações a cada minuto. Essa configuração foi feita dessa forma apenas para demonstrar o funcionamento de uma atualização assíncrona. O ideal seria ter uma tarefa agendada para ser executada em um horário específico. Por esse motivo, deixei o código que implementaria essa lógica comentado no arquivo `/config/celery_app.py`.

Além disso, foi implementado um endpoint utilizando o Django Rest Framework. Esse endpoint permite apenas a consulta dos dados e não permite a realização de outras operações.

Para parar e remover todos os contêineres do Docker Compose, execute:

    
    docker-compose down
    
# teste_brmed
# teste_brmed
