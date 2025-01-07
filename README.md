# ApiScan
# Script de Teste de Segurança de API

## Descrição
**ApiScan** é uma ferramenta automatizada projetada para testar a segurança de APIs RESTful. Ela utiliza especificações OpenAPI e outras fontes para identificar endpoints e realizar testes automatizados, detectando possíveis vulnerabilidades e problemas de segurança com base nas recomendações do OWASP.

### Base para Testes
Para o desenvolvimento e validação da ferramenta, utilizamos como base o projeto [VulnAPI](http://vulnapi.testinvicti.com/) disponibilizado pela **VulnWeb**. Este projeto simula uma API vulnerável, permitindo realizar testes em um ambiente controlado e educacional.

---

## Funcionalidades
### 1. **Carregamento de Especificação OpenAPI**
- Permite o carregamento de uma especificação OpenAPI a partir de um arquivo local ou URL.
- Identifica automaticamente os endpoints disponíveis na API.

### 2. **Autenticação Personalizável**
- Suporte a três métodos de autenticação:
  1. Sem autenticação.
  2. Token Bearer.
  3. Login com credenciais, obtendo o token automaticamente.

### 3. **Teste Automatizado de Endpoints**
- Realiza chamadas para os endpoints especificados, utilizando os métodos HTTP configurados.
- Suporte para parâmetros em rotas e consultas.

### 4. **Salvamento de Respostas**
- Todas as respostas dos endpoints são salvas no arquivo `raw_responses.json`, incluindo:
  - Rota (`route`).
  - Método HTTP (`method`).
  - Resposta bruta (`raw_response`).

### 5. **Relatório em HTML**
- A ferramenta chama automaticamente o script `geraR.py` ao final dos testes para gerar um relatório em HTML.
- Relatório inclui:
  - Rotas testadas.
  - Métodos HTTP.
  - Resumo das respostas brutas.

### 6. **Suporte a Proxy**
- Compatível com ferramentas de análise intermediária como Burp Suite.
- Opção para ativar/desativar o proxy no momento da execução.

---

## Diferenças da Versão Atual (07/01) em Relação à Versão de 03/01

### **Nova Versão (07/01):**
1. **Geração Externa de Relatórios:**
   - A lógica de geração de relatórios foi movida para um script externo, `geraR.py`.
   - A ferramenta principal (`apiscan.py`) agora foca exclusivamente em realizar os testes e salvar as respostas.

2. **Melhoria na Organização do Código:**
   - Estrutura modularizada para melhor manutenção e extensibilidade.
   - Código mais limpo, com separação de responsabilidades.

3. **Relatórios mais Personalizáveis:**
   - O novo script `geraR.py` permite ajustes mais fáceis no design e conteúdo do relatório HTML.

4. **Salvamento Detalhado de Respostas:**
   - As respostas brutas de todos os endpoints são salvas no arquivo `raw_responses.json` para posterior análise.

### **Versão Anterior (03/01):**
1. **Geração Interna de Relatórios:**
   - Relatórios HTML eram gerados diretamente dentro do `apiscan.py`, dificultando alterações e personalizações.

2. **Falta de Modulação:**
   - A lógica de teste e geração de relatório estava centralizada em um único script.

3. **Menos Foco em Análise Bruta:**
   - As respostas brutas não eram salvas para análise detalhada.

---

## Como Usar

### 1. Pré-requisitos
- Python 3.x instalado.
- Biblioteca `requests` e `jinja2`:
  ```bash
  pip install requests jinja2
   ```
### 2. Configuração do Proxy

Caso deseje usar um proxy (como Burp Suite), configure-o no arquivo:

```python
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080" ```
}
```
USE_PROXY = True  # Ative o proxy se necessário.
![inicio](/apiscan_burp.png)
### 3. Execução

1. **Execute o script principal:**
   ```bash
   python apiscan.py
   ```

2. **Siga as instruções fornecidas no terminal para:**
Inserir a URL base da API.
Carregar o arquivo ou URL da especificação OpenAPI.
Configurar o método de autenticação.

3. **Geração de Relatório:**

Após os testes, o script geraR.py será executado automaticamente.
O relatório em HTML será gerado com os detalhes das rotas testadas.

Arquitetura do Projeto
A estrutura do projeto está organizada da seguinte forma:
```
├── apiscan.py      # Script principal para realizar os testes.
├── geraR.py        # Script responsável pela geração do relatório.
├── raw_responses.json  # Arquivo com respostas brutas dos testes.
```

### Exemplo de Relatório
O relatório HTML contém:
```
Rota: O endpoint testado.
Método: O método HTTP utilizado.
Resposta Bruta: As primeiras 200 linhas da resposta do endpoint.
```
### Contribuição
Este projeto está aberto para contribuições. Sinta-se à vontade para enviar sugestões, melhorias ou relatar problemas.

### Referências
[VulnAPI](http://vulnapi.testinvicti.com/)
