# 🌱 API Secundária
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)  
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FFCA28?style=for-the-badge&logo=sqlalchemy&logoColor=black)  
![YFinance](https://img.shields.io/badge/YFinance-purple?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A **API Secundária** é um serviço desenvolvido em Flask que gerencia objetivos de economia (Saving Goals). 
Essa API permite criar, consultar, atualizar e deletar metas de economia cadastradas em um banco de dados. 
Além disso, a API realiza conversão automática de valores para a moeda BRL (Real) utilizando dados da API 
externa [Yahoo Finance](https://pypi.org/project/yfinance/).

---

## 🚀 Funcionalidades

- Criar metas de economia com valor convertido para BRL;
- Listar todas as metas de economia;
- Buscar meta por ID;
- Atualizar meta existente;
- Deletar meta existente.

---

## ⚙️ Instalação e Configuração

### 1. Clone o repositório:
```bash
git clone https://github.com/yoko-takano/mpv-secondary-api.git
cd mpv-secondary-api
```

### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Inicie a aplicação usando Docker:

Certifique-se de que a network `app-network` já existe em seu ambiente Docker com o comando:

```bash
docker network ls
```

Ou crie-a com:

```bash
docker network create app-network
```

E em seguida suba o container:
```bash
docker-compose up --build
```

A API estará disponível em: http://localhost:5000

---

## 📌 Rotas da API Secundária 

As rotas abaixo compõem as funcionalidades de gerenciamento de goals de economia:

**`POST` /goals** - Cria uma meta de economia  
**`GET` /goals** - Lista todas as metas cadastradas  
**`GET` /goals/{goal_id}** - Retorna uma meta específica por ID  
**`PUT` /goals/{goal_id}** - Atualiza uma meta existente  
**`DELETE` goals/{goal_id}** - Remove uma meta do banco de dados  

### 🌐 Integração com a API Externa (`yfinance`)

As rotas `POST /goals` e `PUT /goals/{goal_id}` utilizam a biblioteca `yfinance` para consultar 
o valor atual de ativos financeiros (ações, fundos etc.) no momento da criação ou atualização de uma meta. 
Essa integração garante que o planejamento financeiro do usuário seja feito com base em informações 
atualizadas do mercado.
