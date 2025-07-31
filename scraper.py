
import logging
import cloudscraper
import requests
import os

# Setup de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o cloudscraper
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})

# API Key opcional para ScraperAPI (caso disponível)
SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")

def fetch_html(url: str, use_scraperapi: bool = True) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # Tenta usar cloudscraper primeiro
    try:
        logger.info(f"Tentando cloudscraper para {url}")
        response = scraper.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and "html" in response.headers.get("Content-Type", ""):
            logger.info("HTML válido recebido com cloudscraper")
            return response.text
        else:
            logger.warning("cloudscraper falhou ou retornou conteúdo inválido")
    except Exception as e:
        logger.error(f"Erro com cloudscraper: {e}")

    # Fallback: tenta ScraperAPI se chave estiver disponível
    if use_scraperapi and SCRAPERAPI_KEY:
        try:
            logger.info("Tentando ScraperAPI como fallback")
            proxy_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={url}"
            response = requests.get(proxy_url, timeout=10)
            if response.status_code == 200 and "html" in response.headers.get("Content-Type", ""):
                logger.info("HTML válido recebido com ScraperAPI")
                return response.text
            else:
                logger.warning("ScraperAPI falhou ou retornou conteúdo inválido")
        except Exception as e:
            logger.error(f"Erro com ScraperAPI: {e}")

    # Última tentativa: requests puro com headers
    try:
        logger.info("Tentando requests padrão como última tentativa")
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and "html" in response.headers.get("Content-Type", ""):
            logger.info("HTML recebido com requests padrão")
            return response.text
        else:
            logger.warning("requests padrão falhou ou retornou conteúdo inválido")
    except Exception as e:
        logger.error(f"Erro com requests padrão: {e}")

    logger.error("Falha ao obter HTML da página")
    return ""
