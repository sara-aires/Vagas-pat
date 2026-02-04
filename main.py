import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://www.caraguatatuba.sp.gov.br/pmc/vagas-no-pat/"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload)

def verificar_vagas():
    response = requests.get(URL, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    texto = soup.get_text(separator=" ")

    encontrou_ti = re.search(r"\bti\b", texto, re.IGNORECASE)
    encontrou_info = re.search(r"informática", texto, re.IGNORECASE)
    encontrou_prom = re.search(r"promotor", texto, re.IGNORECASE)
    

    if encontrou_ti or encontrou_info:
        enviar_telegram(
            "🚨 VAGA DE TI DETECTADA!\n\n"
            "Foi encontrada referência a:\n"
            f"{'TI' if encontrou_ti else ''} "
            f"{'Informática' if encontrou_info else ''}\n\n"
            f"{'promotor' if encontrou_info else ''}\n\n"
            f"Link: {URL}"
        )

if __name__ == "__main__":
    verificar_vagas()
