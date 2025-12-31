# **Contexto do Projeto: GoDrive**

## **1\. Visão Geral do Produto**

O **GoDrive** é uma plataforma SaaS e Marketplace que conecta alunos interessados em tirar a CNH (Carteira Nacional de Habilitação) diretamente a instrutores credenciados independentes. O projeto surge no contexto da nova legislação brasileira que flexibiliza a contratação de instrutores.

* **Modelo de Negócio:** Taxa sobre transações (marketplace de aulas) e venda de cursos/material didático (EdTech).  
* **Público-alvo:** Alunos (busca por facilidade e preço) e Instrutores (busca por alunos e gestão financeira).  
* **Escopo:** Nacional (Brasil).

## **2\. Stack Tecnológica**

O sistema foi projetado para alta escalabilidade e concorrência:

* **Mobile (Android/iOS):** React Native (com Expo e TypeScript).  
* **Backend (API):** Python (FastAPI) \- Assíncrono.  
* **Banco de Dados:** PostgreSQL com extensão **PostGIS** (para consultas espaciais eficientes).  
* **Comunicação:**  
  * **REST (HTTP):** Para CRUD padrão (cadastros, pagamentos, cursos).  
  * **WebSockets:** Para telemetria em tempo real (localização do veículo durante a aula).  
* **Infraestrutura:** Docker (previsto), Integração com Gateways de Pagamento e OCR.

## **3\. Arquitetura de Software**

A estrutura do Backend segue uma organização modular para facilitar a manutenção:

back:
```Plaintext
godrive-backend/
├── .env.example                # Variáveis de ambiente (Modelo)
├── .gitignore
├── docker-compose.yml          # Definição do App + Postgres/PostGIS [
├── Dockerfile
├── requirements.txt            # Dependências Python 
├── alembic.ini                 # Configuração de Migrations
├── migrations/                 # Scripts de migração do banco
│
└── app/
    ├── __init__.py
    ├── main.py                 # Ponto de entrada (Inicializa FastAPI) 
    │
    ├── api/                    # Camada de Entrada (Interface HTTP)
    │   └── v1/
    │       ├── router.py       # Centralizador de rotas
    │       └── endpoints/      # Controllers
    │           ├── auth.py     # Login, Refresh Token 
    │           ├── users.py    # CRUD Alunos/Instrutores
    │           ├── rides.py    # Agendamento e Aulas 
    │           ├── payments.py # Webhook Stripe/Pagar.me 
    │           └── courses.py  # LMS 
    │
    ├── core/                   # Configurações do Sistema
    │   ├── config.py           # Settings (Pydantic BaseSettings) 
    │   ├── security.py         # Lógica de Hash e JWT 
    │   └── exceptions.py       # Exceções customizadas
    │
    ├── db/                     # Camada de Infraestrutura de Dados
    │   ├── session.py          # Engine e SessionMaker 
    │   └── base.py             # Base declarativa do SQLAlchemy 
    │
    ├── models/                 # Entidades (Classes que representam tabelas) 
    │   ├── user.py             # User, InstructorProfile
    │   ├── ride.py             # Ride, RideEvent
    │   └── course.py           # Course, Enrollment
    │
    ├── schemas/                # DTOs (Validação e Serialização) 
    │   ├── user.py             # UserCreate, UserResponse
    │   ├── ride.py             # RideCreate, RideResponse
    │   └── common.py           # Schemas reutilizáveis
    │
    ├── repositories/           # Abstração de Acesso a Dados (Pattern Repository)
    │   ├── base.py             # Interface Genérica (CRUDBase)
    │   ├── user_repository.py  # Queries específicas de usuário
    │   └── ride_repository.py  # Queries geoespaciais (PostGIS)
    │
    ├── services/               # Regras de Negócio (O "Cérebro" da aplicação) 
    │   ├── auth_service.py     # Regras de autenticação
    │   ├── ride_matching.py    # Lógica de buscar instrutor no raio X
    │   ├── payment_service.py  # Lógica de Split de pagamento
    │   └── user_service.py
    │
    └── utils/                  # Utilitários puros (Helpers)
        ├── geo.py              # Cálculos auxiliares de distância
        └── validators.py       # Validações de CPF/CNH
```

mobile:
```Plaintext 
godrive-mobile/
├── App.tsx                     # Entrypoint
├── app.json / app.config.ts    # Configuração do Expo
├── package.json
├── tsconfig.json
│
└── src/
    ├── assets/                 # Imagens, fontes, ícones
    │
    ├── components/             # UI Components (Burros/Presentational)
    │   ├── common/             # Botões, Inputs, Cards genéricos
    │   ├── map/                # Componentes relacionados ao Mapa [cite: 14]
    │   └── forms/              # Formulários de Login/Cadastro
    │
    ├── screens/                # Telas completas (Containers)
    │   ├── auth/
    │   │   ├── LoginScreen.tsx
    │   │   └── RegisterScreen.tsx 
    │   ├── student/
    │   │   ├── HomeScreen.tsx      # Mapa principal
    │   │   └── InstructorDetail.tsx 
    │   └── instructor/
    │       └── DashboardScreen.tsx
    │
    ├── navigation/             # Configuração de Rotas
    │   ├── AppNavigator.tsx    # Stack/Tabs 
    │   └── AuthNavigator.tsx
    │
    ├── services/               # Integração com Backend (Pattern Service/Adapter)
    │   ├── api.ts              # Instância do Axios configurada
    │   ├── auth.service.ts     # Classes com métodos estáticos ou singleton
    │   ├── ride.service.ts
    │   └── socket.service.ts   # Gerenciador de WebSocket 
    │
    ├── store/                  # Gerenciamento de Estado Global (Zustand/Context)
    │   ├── useAuthStore.ts     # Sessão do usuário
    │   └── useRideStore.ts     # Estado da corrida atual
    │
    ├── hooks/                  # Logic Encapsulation (React Hooks)
    │   ├── useLocation.ts      # Lógica de permissão e pegar lat/long
    │   └── useForm.ts
    │
    ├── types/                  # Interfaces TypeScript (Modelos do Frontend)
    │   ├── user.ts
    │   ├── ride.ts
    │   └── navigation.ts
    │
    └── utils/                  # Formatadores de data, moeda, máscaras
        └── formatters.ts

```

## **4\. Requisitos Funcionais (Resumo Consolidado)**

### **Módulo de Acesso**

* **Cadastro:** Alunos (simples) e Instrutores (complexo, com upload de CNH, doc do veículo).  
* **Backoffice:** Painel administrativo para validação manual ou automatizada (OCR) dos documentos dos instrutores.

### **Módulo Marketplace & Aulas**

* **Busca Georreferenciada:** Alunos buscam instrutores por raio (km), preço, avaliação e modelo do carro.  
* **Agendamento:** Reserva de horário com status "Pendente" até pagamento. Instrutor gere bloqueios de agenda.  
* **Monitoramento (Real-Time):**  
  * Check-in/Check-out via geolocalização para validar a aula.  
  * Rastreamento via WebSocket (atualização adaptativa: 5s em movimento, 30s parado).  
* **Comunicação:** Chat in-app ou VoIP (Planejado) para comunicação pré-aula.

### **Módulo Financeiro**

* **Pagamentos:** Processamento in-app (Crédito/Pix) via Gateway.  
* **Carteira Digital:** Instrutor visualiza saldo e solicita saque.  
* **Split de Pagamento:** Divisão automática da receita (Taxa GoDrive vs. Valor Instrutor) no momento da transação.

### **Módulo Educacional (LMS)**

* **Conteúdo:** Venda e consumo de cursos extras (Direção Defensiva, Mecânica) e Simulados do DETRAN.  
* **Player:** Reprodução de vídeo com salvamento de progresso.

## **5\. Regras de Negócio Críticas**

1. **Cancelamento:** Reembolso total apenas com 24h de antecedência. Cancelamento tardio implica multa de 50%.  
2. **Veículo:** Deve possuir validação via vistoria ou foto comprovatória.  
3. **Split Fiscal:** Necessidade de emissão de NF sobre a taxa de serviço da plataforma.  
4. **Avaliação Bilateral:** Obrigatória ao fim da aula (Aluno avalia Instrutor e vice-versa).

## **6\. Requisitos Não Funcionais**

* **Segurança:** Criptografia de dados sensíveis (LGPD) e autenticação JWT.  
* **Disponibilidade:** SLA de 99.5%.  
* **Mobile First:** Interface otimizada para uso na rua.  