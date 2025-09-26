import requests
from urllib.parse import urlencode

# Prueba directa con la API de Wikidata para la palabra 'emotions'
def search_wikidata_entity(term):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": term
    }
    headers = {"User-Agent": "entities-extract-bot/1.0 (tu_email@dominio.com)"}
    full_url = f"{url}?{urlencode(params)}"
    print(f"URL de la petición: {full_url}")
    response = requests.get(url, params=params, headers=headers)
    print(f"Código de estado: {response.status_code}")
    print("Respuesta JSON cruda:")
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data.get("search", [])
    return []

if __name__ == "__main__":
    term = "emotions"
    results = search_wikidata_entity(term)
    print(f"Resultados para '{term}':")
    for entity in results:
        print(f"QID: {entity['id']}, Label: {entity['label']}, Description: {entity.get('description', '')}")
    if not results:
        print("No se encontraron entidades.")
