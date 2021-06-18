<h1 align="center">Steuer</h1>

---

<p align="center"> Burocracia é chato, automações duvidosas são legais 😄</p>

## Sobre <a name = "about"></a>

Steuer é um quase-bot em Selenium que emite notas no site da prefeitura de São Paulo
por você.

> "_Quase_ bot?"

Sim! Você vai precisar digitar o captcha na tela do login e o bot não vai clicar
em 'emitir' de fato, por segurança, para que você possa verificar os dados

## Pré-requisitos

Para rodar, você precisa do Python, Poetry e um dos WebDrivers suportados instalados:
- [Geckodriver](https://medium.com/beelabsolutions/baixando-e-configurando-o-geckodriver-no-ubuntu-dc2fe14d91c)
- [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

```
pip install poetry
```

é suficiente para instalar o poetry. O gecko é mais chatinho mas o link na referência
tem informações pra linux. A [página oficial](https://github.com/mozilla/geckodriver)
também tem mais informações. A instalação do Chromedriver é trivial: basta garantir
que o caminho para o binário está no `PATH`

## Instalando

1. Clone esse repositório
2. `poetry install`
3. :fireworks:

## 🎈 Uso

Steuer é uma ferramenta de linha de comando. Você pode customizar o comportamento
dela por flags ou preenchendo o arquivo `exemplo.env` com seus dados e salvando-o
como `secret.env` . Tudo o que você colocar lá será usado como valor padrão.

Um exemplo de uso é:

```
poetry run python steuer --driver=gecko --cnpj=xx.xxx.xxx/xxxx-xx --target=acme --description=compra de bot --value="100,00"
```

Vai preencher uma nota para "acme" com a descrição "compra de bot" no valor de "100,00" utilizando o Geckodriver (Firefox).

O nome do target ― no caso "acme" ― deve estar cadastrado como "apelido de tomador de serviço"
no sistema
