import requests
from bs4 import BeautifulSoup
import validators

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lança um erro para códigos de resposta HTTP 4xx ou 5xx
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao buscar a URL: {e}")
        return None

def analyze_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Verifique a presença de formulários
    forms = soup.find_all('form')
    has_sensitive_form = False

    for form in forms:
        inputs = form.find_all('input')
        has_login_field = any(input_.get('type') in ['password', 'text'] for input_ in inputs)
        is_post_method = form.get('method', '').lower() == 'post'

        if has_login_field and is_post_method:
            has_sensitive_form = True
            break

    # Verifique se há referências a palavras-chave
    keywords = ['salvar', 'credenciais', 'login', 'user', 'senha', 'password', 'store', 'save', 'credentials']
    body_text = soup.get_text().lower()
    found_keywords = any(keyword in body_text for keyword in keywords)

    return has_sensitive_form or found_keywords

def check_ssl(url):
    try:
        response = requests.get(url, timeout=10, verify=True)
        return response.url.startswith('https://')
    except requests.RequestException:
        return False

def check_phishing_database(url):
    # Simulando a verificação em um banco de dados de phishing (Exemplo com PhishTank)
    # Você precisaria de uma chave de API válida e de implementar a chamada real
    return False  # Simulação - retorna sempre False

def main():
    print("Bem-vindo ao Verificador de Phishing!")
    url = input("Insira a URL que deseja verificar: ")

    if not validators.url(url):
        print("URL inválida. Verifique e tente novamente.")
        return

    # Verificação de SSL
    ssl_valid = check_ssl(url)
    if not ssl_valid:
        print("⚠️ O site não tem um certificado SSL válido. ⚠️")
        return

    # Verificação no banco de dados de phishing
    is_phishing_database = check_phishing_database(url)
    if is_phishing_database:
        print("⚠️ O site foi identificado como um site de phishing. ⚠️")
        return

    # Verificação de HTML
    html = fetch_html(url)
    if html:
        is_phishing_html = analyze_html(html)
        if is_phishing_html:
            print("⚠️ PÁGINA POTENCIALMENTE DE PHISHING ⚠️")
        else:
            print("✅ A página parece segura ✅")
    else:
        print("Erro ao buscar a URL. Verifique se a URL é válida.")

if __name__ == "__main__":
    main()
