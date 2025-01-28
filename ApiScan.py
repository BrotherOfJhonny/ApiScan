import requests
import json
import urllib3
import time
from datetime import datetime
from geraR import generate_report  # Importando a função generate_report do script geraR.py

# Desativar avisos de HTTPS não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração inicial do proxy (exemplo: Burp Suite)
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

USE_PROXY = False  # Variável para ativar/desativar o proxy

def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {message}")

# Função para exibir o banner ASCII
def display_banner():
    banner = """
     █████╗ ██████╗ ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██║██╔════╝██╔════╝██╔══██╗████╗  ██║
    ███████║██████╔╝██║███████╗██║     ███████║██╔██╗ ██║
    ██╔══██║██╔═══╝ ██║╚════██║██║     ██╔══██║██║╚██╗██║
    ██║  ██║██║     ██║███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """
    print(banner)

# Função para exibir a mensagem de "aguarde" com animação
def display_loading_message():
    message = "Executando testes, aguarde"
    print(message, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")

# Função para carregar a especificação OpenAPI ou extrair de uma URL
def load_openapi_spec(file_or_url):
    if file_or_url.startswith("http://") or file_or_url.startswith("https://"):
        print("Detectada URL. Verificando o tipo de resposta...")
        response = requests.get(file_or_url, proxies=PROXIES if USE_PROXY else None, verify=False)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            print("Resposta JSON detectada. Carregando especificação OpenAPI...")
            return response.json().get("paths", {})
        else:
            print("[ERRO] O conteúdo retornado não é JSON. Verifique a URL fornecida.")
            return None

    else:
        print("Carregando especificação OpenAPI de um arquivo local...")
        with open(file_or_url, 'r') as file:
            return json.load(file).get("paths", {})

# Função para autenticação via login
def login_for_token(base_url):
    username = input("Digite o nome de usuário para login: ").strip()
    password = input("Digite a senha: ").strip()
    login_url = f"{base_url}/api/login"

    try:
        response = requests.post(
            login_url,
            json={"username": username, "password": password},
            proxies=PROXIES if USE_PROXY else None,
            verify=False
        )
        response.raise_for_status()
        token = response.json().get("token")
        if token:
            print("Autenticação bem-sucedida. Token recebido.")
            return {"Authorization": f"Bearer {token}"}
        else:
            print("Falha ao obter o token. Verifique suas credenciais.")
            return None
    except Exception as e:
        print(f"Erro durante a autenticação: {e}")
        return None

# Função para configurar autenticação
def configure_authentication(base_url):
    auth_method = input("Escolha o método de autenticação (1: Nenhuma, 2: Token Bearer, 3: Login): ").strip()

    if auth_method == "1":
        return None
    elif auth_method == "2":
        token = input("Digite o token Bearer: ").strip()
        return {"Authorization": f"Bearer {token}"}
    elif auth_method == "3":
        return login_for_token(base_url)
    else:
        print("Opção inválida. Nenhuma autenticação será usada.")
        return None

# Função para ativar/desativar o uso de proxy
def configure_proxy():
    global USE_PROXY
    use_proxy_input = input("Deseja ativar o uso de proxy? (s/n): ").strip().lower()
    if use_proxy_input == "s":
        USE_PROXY = True
        print("Proxy ativado.")
    else:
        USE_PROXY = False
        print("Proxy desativado.")

# Função para testar as rotas
def test_api_routes(base_url, paths, headers):
    results = []
    raw_responses = []  # Lista para armazenar respostas brutas

    if not isinstance(paths, dict):
        print("[ERRO] Nenhum endpoint encontrado para testar.")
        return results

    print("Endpoints encontrados:")
    for route, methods in paths.items():
        print(f"Rota: {route}")
        for method, details in methods.items():
            print(f"  Método: {method}")

            # Preparar URL e parâmetros
            params = {}
            for param in details.get("parameters", []):
                if param.get("in") == "path" and param.get("required"):
                    params[param["name"]] = param.get("schema", {}).get("default", "1")
                if param.get("in") == "query" and param.get("required"):
                    params[param["name"]] = "test"

            url = f"{base_url.rstrip('/')}/{route.lstrip('/').format(**params)}"
            try:
                request_kwargs = {
                    "headers": headers,
                    "proxies": PROXIES if USE_PROXY else None,
                    "verify": False
                }
                print(f"[INFO] Testando endpoint: {method.upper()} {url}")
                response = requests.request(method.upper(), url, **request_kwargs)

                results.append({
                    "route": route,
                    "method": method.upper(),
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "response": response.text
                })

                # Armazenar resposta bruta
                raw_responses.append({
                    "route": route,
                    "method": method.upper(),
                    "raw_response": response.text
                })

            except Exception as e:
                results.append({
                    "route": route,
                    "method": method.upper(),
                    "error": str(e)
                })

    return results

# Função principal para executar os testes e gerar relatório
def main():
    display_banner()
    base_url = input("Digite a URL base da API: ").strip()
    configure_proxy()

    paths = load_openapi_spec(input("Digite o caminho do arquivo OpenAPI ou URL: ").strip())
    headers = configure_authentication(base_url)

    display_loading_message()
    results = test_api_routes(base_url, paths, headers)

    log_message("Testes concluídos. Gerando relatório...")

    # Chamar a função diretamente para gerar o relatório
    generate_report(results)

    # Resumo
    log_message("Resumo:")
    log_message(f"- Endpoints testados: {len(results)}")
    log_message(f"- Sucessos: {sum(1 for r in results if r.get('status_code') and r['status_code'] < 400)}")
    log_message(f"- Falhas: {sum(1 for r in results if r.get('status_code') and r['status_code'] >= 400)}")

if __name__ == "__main__":
    main()
