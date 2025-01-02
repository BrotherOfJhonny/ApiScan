import requests
import json
from jinja2 import Template
import urllib3

# Desativar avisos de HTTPS não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração do proxy (exemplo: Burp Suite)
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

USE_PROXY = False  # Variável para (True)ativar/(False)desativar o proxy

# Carregar a especificação OpenAPI
def load_openapi_spec(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Função para construir parâmetros automaticamente
def build_params(args):
    params = {}
    if not args:
        return params

    for param, details in args.items():
        if "default" in details:
            params[param] = details["default"]
        elif "type" in details:
            if details["type"] == "string":
                params[param] = "example"
            elif details["type"] == "integer":
                params[param] = 1
            elif details["type"] == "boolean":
                params[param] = True
            elif details["type"] == "array":
                params[param] = []
            elif details["type"] == "object":
                params[param] = {}
    return params

# Função para testar as rotas
def test_api_routes(base_url, routes):
    results = []

    for route, details in routes.items():
        methods = details.get("methods", [])
        endpoints = details.get("endpoints", [])
        url = f"{base_url}{route}"

        for endpoint in endpoints:
            args = endpoint.get("args", {})
            params = build_params(args)

            for method in methods:
                method = method.upper()

                try:
                    # Configurar a requisição com ou sem proxy
                    request_kwargs = {
                        "params": params if method == "GET" else None,
                        "json": params if method in ["POST", "PUT", "PATCH", "DELETE"] else None,
                        "proxies": PROXIES if USE_PROXY else None,
                        "verify": False,
                        "allow_redirects": True
                    }

                    if method == "GET":
                        response = requests.get(url, **request_kwargs)
                    elif method == "POST":
                        response = requests.post(url, **request_kwargs)
                    elif method == "PUT":
                        response = requests.put(url, **request_kwargs)
                    elif method == "PATCH":
                        response = requests.patch(url, **request_kwargs)
                    elif method == "DELETE":
                        response = requests.delete(url, **request_kwargs)
                    else:
                        continue

                    # Analisar o cabeçalho da resposta
                    if response.status_code == 301:
                        new_url = response.headers.get("Location")
                        if new_url:
                            response = requests.get(new_url, **request_kwargs)

                    result = {
                        "route": route,
                        "method": method,
                        "status_code": response.status_code,
                        "response_time": response.elapsed.total_seconds(),
                        "response": response.json() if response.headers.get("Content-Type", "").startswith("application/json") else response.text
                    }

                    # Validar possíveis problemas OWASP
                    if response.status_code == 401:
                        result["security_warning"] = "A rota requer autenticação."
                    elif response.status_code == 403:
                        result["security_warning"] = "Acesso não autorizado. Verificar permissões."
                    elif response.status_code == 500:
                        # Verificar se existe uma página válida apesar do erro 500
                        if response.text:
                            result["security_warning"] = "Erro interno no servidor, mas há conteúdo válido na resposta."
                        else:
                            result["security_warning"] = "Erro interno no servidor. Pode indicar validação de dados inadequada."

                    results.append(result)

                except Exception as e:
                    results.append({
                        "route": route,
                        "method": method,
                        "error": str(e)
                    })

    return results

# Função para gerar relatório HTML
def generate_html_report(results, output_path):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>APISCAN Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .success { color: green; }
            .failure { color: red; }
        </style>
    </head>
    <body>
        <h1>API Test Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Route</th>
                    <th>Method</th>
                    <th>Status Code</th>
                    <th>Response Time (s)</th>
                    <th>Security Warning</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results if result.get('status_code') is not none %}
                <tr>
                    <td>{{ result.route }}</td>
                    <td>{{ result.method }}</td>
                    <td class="{{ 'success' if result.status_code < 400 else 'failure' }}">{{ result.status_code }}</td>
                    <td>{{ result.response_time }}</td>
                    <td>{{ result.security_warning if result.security_warning else '' }}</td>
                </tr>
                {% endfor %}
                {% for result in results if result.get('status_code') is none %}
                <tr>
                    <td>{{ result.route }}</td>
                    <td>{{ result.method }}</td>
                    <td colspan="3" class="failure">Error: {{ result.error }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    template = Template(html_template)
    html_content = template.render(results=results)

    with open(output_path, "w") as file:
        file.write(html_content)

# Exemplo de uso
def main():
    openapi_path = "openapi.json"  # Substitua pelo caminho correto
    spec = load_openapi_spec(openapi_path)
    base_url = "https://meusite_teste.net"  # Substitua pela URL base correta

    # Obter rotas
    routes = spec.get("routes", {})

    # Testar as rotas
    results = test_api_routes(base_url, routes)

    # Gerar relatório em HTML
    output_path = "api_test_report.html"
    generate_html_report(results, output_path)
    print(f"Relatório gerado em: {output_path}")

if __name__ == "__main__":
    main()
