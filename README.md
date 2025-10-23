# 🚀 POWER MOTO GROUP - API de Confecção de Orçamentos

Este projeto visa desenvolver uma API robusta e eficiente para a **geração e gestão de orçamentos** da empresa **POWER MOTO GROUP**. O principal objetivo é digitalizar e acelerar o processo manual de confecção de orçamentos, garantindo um formato padronizado, e estabelecer uma base de dados centralizada para itens e registros de pedidos/orçamentos.

A adoção desta API permitirá a confecção de orçamentos de forma mais rápida e a manutenção de um histórico organizado e acessível.

## 🛠️ Tecnologias Utilizadas

O backend da API foi desenvolvido utilizando as seguintes tecnologias:

| Categoria | Tecnologia | Detalhes |
| :--- | :--- | :--- |
| **Linguagem** | Python | Linguagem principal para desenvolvimento da API. |
| **Banco de Dados** | PostgreSQL | SGBD relacional robusto para armazenamento de dados de clientes, itens e orçamentos. |
| **ORM** | SQLAlchemy | Biblioteca Python para mapeamento objeto-relacional (ORM), facilitando a interação com o PostgreSQL. |

## 📐 Formato Padrão do Orçamento

Para garantir clareza e padronização, cada item do orçamento gerado pela API segue um formato estruturado que inclui informações de identificação, valor e prazo de entrega.

### Estrutura de Exibição

| Campo | Modelo | Exemplo |
| :--- | :--- | :--- |
| **Item** | `Nome do item (código da peça) - <número de unidades> UNIDADES` | `Filtro de óleo (JG571014) - 2 UNIDADES` |
| **Valor** | `Valor: R$ <valor do item>` | `Valor: R$ 42,76` |
| **Prazo** | **Estoque:** `Prazo: À pronta entrega` | `Prazo: À pronta entrega` |
| **Prazo** | **Encomenda:** `Prazo estimado: <dias> úteis (encomenda)` | `Prazo estimado: 7 úteis (encomenda)` |

**Exemplo de Orçamento (Item Único):**
```
Filtro de óleo (JG571014) 
Valor: R$ 21,38
Prazo: À pronta entrega
```

## 🗺️ Rotas da API (Endpoints)

A API é dividida em módulos que permitem a gestão completa dos dados essenciais para a confecção dos orçamentos (Clientes, Itens, Itens do Pedido e Pedidos/Orçamentos).

### Clientes

Gerenciamento de informações dos clientes.

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/clientes` | `GET` | Lista todos os clientes cadastrados. |
| `/clientes` | `POST` | Cria um novo cliente. |
| `/clientes/{id}` | `GET` | Busca um cliente específico por ID. |
| `/clientes/{id}` | `PUT` | Atualiza as informações de um cliente. |
| `/clientes/{id}` | `DELETE` | Remove um cliente (soft delete recomendado). |

### Itens (Estoque/Catálogo)

Gerenciamento do catálogo de produtos e peças, identificados pelo SKU.

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/itens` | `GET` | Lista todos os itens do catálogo. |
| `/itens` | `POST` | Cadastra um novo item. |
| `/itens/{SKU}` | `GET` | Busca um item específico pelo **SKU** (código da peça). |
| `/itens/{SKU}` | `PUT` | Atualiza as informações de um item. |
| `/itens/{SKU}` | `DELETE` | Remove um item do catálogo. |

### Itens do Pedido (Associação Pedido ↔ Item)

Gerenciamento dos itens que compõem um pedido específico, incluindo quantidade e valores no momento do orçamento.

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/itensPedido` | `GET` | Lista todos os itens associados a pedidos. |
| `/itensPedido` | `POST` | Adiciona um item a um pedido/orçamento existente. |
| `/itensPedido/{id}` | `GET` | Busca um item de pedido específico por ID. |
| `/itensPedido/{id}` | `PUT` | Atualiza a quantidade ou informações do item no pedido. |
| `/itensPedido/{id}` | `DELETE` | Remove um item de um pedido. |

### Pedidos (Orçamentos)

Gerenciamento dos orçamentos e seus status.

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/pedidos` | `GET` | Lista todos os orçamentos/pedidos. |
| `/pedidos` | `POST` | Inicia a criação de um novo orçamento. |
| `/pedidos/{id}` | `GET` | Busca um orçamento específico por ID. |
| `/pedidos/{id}` | `PUT` | Atualiza informações do orçamento (ex: status). |
| `/pedidos/{id}` | `DELETE` | Cancela/Remove um orçamento. |
