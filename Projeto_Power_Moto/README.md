# Projeto Python – Sistema de Confecção de Orçamentos

Este projeto tem como objetivo desenvolver um sistema para a geração de orçamentos da empresa *POWER MOTO GROUP*. O sistema permitirá a criação de orçamentos de forma estruturada, seguindo um formato padronizado para melhor organização e compreensão.
Com esse projeto viso realizar os orçamentos manuais de forma mais rápida, e estabelecer um banco de dados para os ites e o registro dos orçamentos

##### Formato do Orçamento:
Cada item do orçamento seguirá o seguinte modelo:

Nome do item (código da peça) - <número de unidades> UNIDADES *(Caso tenha mais de uma unidade)*
Valor: R$ <valor do item>

*Casos de prazo:*
- Itens em estoque: 
Prazo: À pronta entrega "(última unidade)" - Caso seja última unidade

- Itens em estoques diferentes:
Prazo estimado: <dias> úteis (transferência) "(última unidade)" - Caso seja última unidade

- Itens de encomenda:
Prazo estimado: <dias> úteis (encomenda)

Exemplo de orçamento:

```
Filtro de óleo (JG571014)
Valor: R$ 21,38
Prazo: À pronta entrega
```

## Tecnologias:

O projeto será feito via Pyhton, para o banco de dados vamos utilizar a bibilioteca SQLALCHEMY

[![UML](Diagrama.png)]