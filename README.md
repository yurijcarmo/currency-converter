# API de Conversão Monetária

## Descrição do Projeto

Este projeto consiste em uma API de conversão monetária que permite converter entre diferentes moedas, tendo o dólar americano (USD) como moeda de referência.

## Funcionamento

Ao receber uma solicitação com a moeda de origem, o valor a ser convertido e a moeda final desejada, a API realiza os seguintes passos:

### Atualização das Taxas de Câmbio:

- Verifica se as taxas de câmbio estão atualizadas e, se necessário, consulta as APIs de cotações para obter as taxas mais recentes.

### Cálculo da Conversão:

- O valor informado é convertido para USD usando a taxa de câmbio da moeda de origem em relação ao USD.
- Em seguida, o valor em USD é convertido para a moeda final desejada usando a taxa de câmbio da moeda final em relação ao USD.

## Endpoints Disponíveis

- `/convert_currency`: Endpoint para realizar a conversão monetária. Parâmetros: `from` (moeda de origem), `to` (moeda final) e `amount` (valor a ser convertido).
- `/currencies`: Endpoint para obter a lista de moedas permitidas para conversão.

## Expressão do Cálculo

O cálculo da conversão é feito conforme as seguintes expressões matemáticas:

- `amount_usd = amount * rate_from_currency`
- `amount_to_currency = amount_usd * rate_to_currency`

## Configuração da Chave da API

Dentro do diretório `backend`, existe um arquivo `.env` que contém uma variável chamada `API_KEY`. Essa chave é necessária para acessar a API de conversão monetária fornecida pelo FastForex, a qual permite consultar os dados necessários para realizar as conversões usando o dólar americano (USD) como moeda de lastro.

Por padrão, forneci uma chave de API gratuita, que pode expirar em breve devido às limitações do plano gratuito. No entanto, você pode gerar sua própria chave gratuita de 7 dias visitando [este link](https://www.fastforex.io/?gad_source=1&gclid=CjwKCAjwnv-vBhBdEiwABCYQA_jMOXCA5dtuFBjou5BpgVl4qBZNacWHhwldV1ho-TsJwDxtxgjNABoCgcIQAvD_BwE) e seguindo as instruções fornecidas no site.

Se preferir, você também pode optar por adquirir uma chave de API do plano pago para obter acesso contínuo ao serviço. Isso permite que você use o projeto sem se preocupar com a expiração da chave.

Lembre-se de substituir o valor da variável `API_KEY` no arquivo `.env` pela chave que você gerou, garantindo que o serviço de conversão monetária funcione corretamente.

## Observações

- As taxas de câmbio são atualizadas regularmente para fornecer cotações precisas e atualizadas.
- O cálculo da conversão utiliza o dólar americano como moeda de referência.


# Instruções de Instalação e Execução

## Pré-requisitos

**Instruções de Instalação e Execução**

**Pré-requisitos**

Para executar este projeto, deve-se ter o Docker e o Docker Compose instalados em seu sistema operacional. Durante o desenvolvimento deste projeto, os testes foram realizados com as seguintes versões:

- Docker version 25.0.4, build 1a576c5
- Docker Compose version 1.22.0, build f46880fe

Embora essas versões tenham sido usadas para testes, não é estritamente necessário ter exatamente essas versões instaladas. Recomenda-se ter versões recentes para garantir a compatibilidade e evitar possíveis problemas.

Se ainda não foram instalados, siga os links abaixo para instalar:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Certifique-se também de ter o Git instalado para clonar o repositório.

## Clonando o Repositório

```python
git@github.com:yurijcarmo/currency-converter.git
```

## Executando o Projeto

Após clonar o repositório, navegue até a raiz do projeto e execute o seguinte comando no terminal:

```python
docker-compose up
```
Isso iniciará os contêineres Docker e configurará o ambiente do projeto.

## Acessando o Projeto

Depois que o Docker Compose terminar de construir e iniciar os contêineres, pode-se acessar o projeto em seu navegador da web em:

[http://localhost:3000](http://localhost:3000)

Isso é tudo! Agora você está pronto para começar a usar o projeto.

# Mais Detalhes:

## Executando Testes Unitários do Backend

Para executar os testes unitários do backend, siga os passos abaixo:

1. Abra uma nova aba do terminal.

2. Navegue até a raiz do projeto.

3. Execute os seguintes comandos:

```bash
docker exec -it django sh
python manage.py test
```

Isso acessará o container do Django e executará os testes unitários do backend.

## Executando Testes Unitários do Frontend

Para executar os testes unitários do frontend, siga os passos abaixo:

1. Abra uma nova aba do terminal.

2. Navegue até a raiz do projeto.

3. Execute o seguinte comando para acessar o container do frontend:

```bash
docker exec -it frontend sh
```

Isso abrirá um shell dentro do container do frontend.

4. Dentro do shell do container, execute o seguinte comando para executar os testes utilizando o Jest:

```bash
yarn jest
```

Isso iniciará a execução dos testes unitários do frontend e exibirá os resultados no terminal.