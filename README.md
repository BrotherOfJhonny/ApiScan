# ApiScan
# Script de Teste de Segurança de API

## Visão Geral
Este script é uma ferramenta em Python projetada para automatizar a avaliação de segurança de APIs. Ele utiliza a especificação OpenAPI para extrair rotas, métodos e parâmetros da API a serem testados. O objetivo principal é identificar possíveis vulnerabilidades e configurações incorretas em APIs, simulando requisições e analisando respostas.

## Funcionalidades
- **Construção Dinâmica de Parâmetros**: Constrói automaticamente os parâmetros das requisições com base na especificação OpenAPI.
- **Testes com Parâmetro `id`**: Realiza testes utilizando tanto strings como valores numéricos entre 1 e 9 para o campo `id`.
- **Suporte a Métodos HTTP**: Testa rotas usando vários métodos HTTP (GET, POST, PUT, PATCH, DELETE).
- **Integração com Proxy**: Permite redirecionar o tráfego através de um proxy (por exemplo, Burp Suite) para inspeção mais aprofundada.
- **Manipulação de Redirecionamentos**: Segue redirecionamentos HTTP 301 para testar o destino final da requisição.
- **Análise de Erros**: Identifica respostas válidas mesmo em casos de erros HTTP 500.
- **Geração de Relatório em HTML**: Resume os resultados dos testes em um relatório HTML detalhado e visualmente atrativo.
- **Diretrizes OWASP**: Destaca vulnerabilidades comuns em APIs, como problemas de autenticação, autorização e validação de dados.
- **Interatividade com Usuário**: Exibe um banner ASCII e uma mensagem de progresso animada durante a execução dos testes.

## Objetivos
- Automatizar os testes de segurança em APIs para economizar tempo e melhorar a cobertura.
- Identificar possíveis vulnerabilidades de segurança, como:
  - Autenticação ausente ou fraca.
  - Falta de verificações adequadas de autorização.
  - Redirecionamentos configurados incorretamente.
  - Exposição de dados sensíveis em erros do servidor.
- Fornecer insights acionáveis por meio de um relatório HTML compreensivo.

## Como Usar

### Pré-requisitos
- Python 3.8+
- Bibliotecas necessárias:
  - `requests`
  - `jinja2`

Instale as dependências:
```bash
pip install requests jinja2
```

### Configuração
1. **Defina o Caminho do Arquivo OpenAPI**:
   Atualize a variável `openapi_path` no script para apontar para o arquivo de especificação OpenAPI.

2. **Defina a URL Base da API**:
   Modifique a variável `base_url` para corresponder à URL base da API que você deseja testar.

3. **Configuração do Proxy**:
   Ative o roteamento por proxy definindo `USE_PROXY = True` e configure o dicionário `PROXIES` com os detalhes do seu proxy (ex.: Burp Suite).

### Execução
Execute o script:
```bash
python ApiScan.py
```
![inicio](/apiscan_inicio.png)
### Saída
- **Logs no Console**: Mostra o progresso dos testes e informações básicas, incluindo uma animação de progresso amigável.
- **Relatório em HTML**: Um arquivo chamado `api_test_report.html` é gerado no diretório do script. Ele inclui:
  - Rotas e métodos testados.
  - Códigos de status e tempos de resposta.
  - Parâmetros utilizados em cada requisição.
  - Avisos de segurança (ex.: autenticação ausente, problemas de manipulação de erros).

![relatorio](/apiscan_relatorio.png)
## Benefícios
- Identifique rapidamente lacunas de segurança em APIs.
- Gere relatórios detalhados e compartilháveis para partes interessadas.
- Integre com proxies como Burp Suite para testes avançados.
- Siga as melhores práticas alinhadas às diretrizes OWASP.

## Exemplo de Caso de Uso
1. Você possui uma API definida com uma especificação OpenAPI.
2. Você deseja testar:
   - Se todas as rotas exigem autenticação adequada.
   - Como a API lida com dados incorretos.
   - Se os erros do servidor expõem informações sensíveis.
3. Execute este script para automatizar os testes e analise o relatório gerado para obter insights.

---

Para quaisquer dúvidas ou contribuições, sinta-se à vontade para abrir um pull request ou relatar um problema!

