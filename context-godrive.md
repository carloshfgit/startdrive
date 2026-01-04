# **Contexto do Projeto: UDrive**

## **1\. Visão Geral do Produto**

O **GoDrive** é uma plataforma SaaS e Marketplace que conecta alunos interessados em tirar a CNH (Carteira Nacional de Habilitação) diretamente a instrutores credenciados independentes. O projeto surge no contexto da nova legislação brasileira que flexibiliza a contratação de instrutores.

* **Modelo de Negócio:** Taxa sobre transações (marketplace de aulas) e venda de cursos/material didático (EdTech).  
* **Público-alvo:** Alunos (busca por facilidade e preço) e Instrutores (busca por alunos e gestão financeira).  
* **Escopo:** Nacional (Brasil).

## **2\. Stack Tecnológica**

### **📱 Mobile (Frontend)**

O foco atual do desenvolvimento será nesta stack:

* **Framework:** **React Native** (com **Expo** Managed Workflow) — para agilidade e compatibilidade iOS/Android.  
* **Linguagem:** **TypeScript** — para tipagem estática e segurança no código.  
* **Gerenciamento de Estado:** **Zustand** — escolhido pela simplicidade e performance (em vez de Redux).  
* **Mapas:** **react-native-maps** — para a visualização de instrutores e rastreamento da aula.  
* **Comunicação API:** **Axios** — cliente HTTP para requisições REST.  
* **Multimídia:** **expo-av** (ou YouTube Embed) — para o player de vídeo das aulas teóricas.

  ### **⚙️ Backend (API)**

Já estruturado e funcional (Fase 5):

* **Linguagem:** **Python 3.10+**.  
* **Framework Web:** **FastAPI** — assíncrono e de alta performance.  
* **Banco de Dados:** **PostgreSQL** com a extensão **PostGIS** — essencial para as buscas geoespaciais (raio de km).  
* **ORM:** **SQLAlchemy** — para interação com o banco de dados.  
* **Comunicação Real-Time:** **WebSockets** — para telemetria e rastreamento do veículo ao vivo.

  ### **🏗️ Infraestrutura e Ferramentas**

* **Containerização:** **Docker** e Docker Compose — para rodar o backend, banco e Redis.  
* **Cache:** **Redis** — para otimizar a busca de instrutores e performance.  
* **Pagamentos:** **Stripe** — para processamento de cartões e split de pagamentos.  
* **Autenticação:** **JWT (JSON Web Tokens)** — para segurança nas sessões de usuário.  
* **Validação:** **Pydantic** — para garantir a integridade dos dados trafegados.

Essa stack foi escolhida para garantir **alta escalabilidade** (graças ao FastAPI e PostGIS) e uma **experiência mobile fluida** (com React Native e Expo).

## **3\. Requisitos Funcionais (Resumo Consolidado)**

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

## **4\. Regras de Negócio Críticas**

1. **Cancelamento:** Reembolso total apenas com 24h de antecedência. Cancelamento tardio implica multa de 50%.  
2. **Veículo:** Deve possuir validação via vistoria ou foto comprovatória.  
3. **Split Fiscal:** Necessidade de emissão de NF sobre a taxa de serviço da plataforma.  
4. **Avaliação Bilateral:** Obrigatória ao fim da aula (Aluno avalia Instrutor e vice-versa).

## **5\. Requisitos Não Funcionais**

* **Segurança:** Criptografia de dados sensíveis (LGPD) e autenticação JWT.  
* **Disponibilidade:** SLA de 99.5%.  
* **Mobile First:** Interface otimizada para uso na rua.