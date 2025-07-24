Com certeza\! Mantive a essência das suas excelentes observações técnicas, mas ajustei a linguagem para um tom mais profissional e direto, ideal para a avaliação de um recrutador.

Aqui está a versão reescrita do seu README:

-----

# **Portal Stream: Sistema de Vendas**

### *Projeto desenvolvido para o Teste de Aptidão da SEMEQ*

## Visão Geral

O Portal Stream é uma aplicação web completa para gestão de vendas, desenvolvida como parte de um processo de avaliação técnica. O sistema demonstra a implementação de funcionalidades essenciais de um e-commerce, com foco em boas práticas de desenvolvimento, qualidade de código e uma arquitetura robusta.

### Funcionalidades Principais

  * **Registro de Vendas:** Permite criar vendas detalhadas, associando produtos, comprador, data e endereço de entrega.
  * **Consulta de Endereço via API:** Integração com a API **ViaCEP** para preenchimento automático do endereço a partir do CEP.
  * **Histórico de Compras:** Interface para que os usuários consultem suas compras anteriores.
  * **Busca de Produtos:** Funcionalidade de busca dinâmica na tela de consulta.
  * **Múltiplos Fornecedores:** Flexibilidade para associar diversos fornecedores a uma mesma venda.
  * **Experiência de Usuário Aprimorada:** O subtotal da venda é atualizado dinamicamente via **HTMX**, eliminando a necessidade de recarregar a página.
  * **Design Responsivo:** Layout construído com **Bootstrap 5**, garantindo usabilidade em diferentes dispositivos.

### Qualidade de Código e Testes

  * **Testes Unitários:** Cobertura de testes para as principais regras de negócio.
  * **Linting e Formatação:** O **Ruff** é utilizado para garantir um padrão de código consistente e limpo.
  * **Tipagem Estática:** O **MyPy** é aplicado para aumentar a robustez e prevenir erros de tipo.

-----

## Notas de Arquitetura e Design

Durante o desenvolvimento, algumas decisões importantes foram tomadas para garantir a qualidade e a manutenibilidade do projeto:

1.  **Arquitetura e Django:** Embora conceitos de Arquitetura Limpa tenham sido considerados, optei por seguir os padrões de projeto consolidados do Django. Esta abordagem garante a manutenibilidade e facilita a colaboração, alinhando-se às melhores práticas da comunidade Django e evitando complexidade desnecessária na estrutura de pastas.

2.  **Estratégia de Testes:** A estratégia atual foca em testes unitários para validar a lógica de negócio principal. Com mais tempo e recursos, o escopo seria expandido para incluir testes de integração e E2E (End-to-End), utilizando um banco de dados em memória para simular cenários complexos e validar o fluxo completo da aplicação.

3.  **Análise sobre a Escolha do Banco de Dados:** Foi feita uma análise crítica sobre a sugestão de integrar um banco de dados NoSQL como o MongoDB. Para o caso de uso de armazenar um "snapshot" do produto no momento da venda, a introdução de um segundo banco de dados poderia gerar problemas de consistência eventual e aumentar a latência. Uma solução mais robusta e integrada seria utilizar o tipo de dado `JSONB` nativo do PostgreSQL. Essa abordagem mantém a consistência transacional e a simplicidade da arquitetura de dados.

-----

## Stack Tecnológico

| Categoria | Tecnologia | Justificativa |
| :--- | :--- | :--- |
| **Backend** | Python 3.13, Django | Base sólida e produtiva para o desenvolvimento web, utilizando uma versão recente da linguagem. |
| **Frontend** | HTML5, Bootstrap 5, HTMX | Interface reativa e responsiva. HTMX foi adicionado para criar interações dinâmicas sem a complexidade de um framework JavaScript completo. |
| **Banco de Dados** | PostgreSQL (via Docker) | Um sistema de banco de dados relacional poderoso e confiável, ideal para aplicações transacionais. |
| **Conteinerização** | Docker, Docker Compose | Garante um ambiente de desenvolvimento consistente e reprodutível, simplificando o setup e o deploy. |
| **Qualidade de Código** | Ruff, MyPy | Ferramentas modernas e eficientes para linting, formatação e checagem de tipos estática em projetos Python. |
| **Dependências** | `uv` | Adotado para um gerenciamento de dependências mais seguro, gerando um "lock file" que previne inconsistências entre ambientes. |

-----

## Pré-requisitos

  * Python 3.13+
  * Docker & Docker Compose
  * Git

-----

## Instalação e Execução Local

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/ViniciusCostaGandolfi/DESAFIO_SEMEC.git
    cd DESAFIO_SEMEC
    ```

2.  **Crie e ative o ambiente virtual:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências com `uv`:**

    ```bash
    pip install --upgrade pip uv
    uv pip install -r requirements.txt
    ```

    *Nota: O `uv` gera o `requirements.txt` a partir do `requirements.in`, garantindo o lock das versões das dependências.*

4.  **Inicie os serviços com Docker Compose:**

    ```bash
    docker-compose up -d
    ```

    *Este comando irá iniciar o contêiner do PostgreSQL.*

5.  **Aplique as migrações do banco de dados:**

    ```bash
    python manage.py migrate
    ```

6.  **Crie um superusuário (opcional):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor de desenvolvimento:**

    ```bash
    uvicorn core.asgi:application --reload
    ```

    A aplicação estará disponível em `http://localhost:8000`.

-----

## Testes e Qualidade de Código

  * **Executar testes unitários e ver cobertura:**

    ```bash
    coverage run manage.py test
    coverage report
    ```

  * **Verificar formatação e lint com Ruff:**

    ```bash
    ruff check .
    ```

  * **Executar checagem de tipos com MyPy:**

    ```bash
    mypy .
    ```

-----

## Screenshots

### Autenticação e Gestão

| Tela de Login | Histórico de Vendas | Detalhes da Venda |
| :---: | :---: | :---: |
| ![Tela de Login](screenshots/login.png) | ![Histórico de Vendas](screenshots/list_sales.png) | ![Detalhes da Venda](screenshots/detail_sale.png) |

| Tela de Registro | Modal de Exclusão | Modal de Sucesso |
| :---: | :---: | :---: |
| ![Tela de Registro](screenshots/register.png) | ![Excluir Venda](screenshots/delete_sale.png) | ![Modal de Sucesso](screenshots/sucess_modal.png) |

---

## Fluxo de Criação de Venda (Passo a Passo)

### Passo 1: Seleção de Produtos

![Passo 1: Seleção de Produtos](screenshots/sale_step_products.png)

---

### Passo 2: Endereço de Entrega

![Passo 2: Endereço de Entrega](screenshots/sale_step_address.png)

---

### Passo 3: Resumo Final da Venda

![Passo 3: Resumo Final da Venda](screenshots/sale_step_summary.png)
