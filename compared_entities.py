import pandas as pd
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Cabecera obligatoria para Wikidata
HEADERS = {"User-Agent": "entities-extract-bot/1.0 (pichu2707@gmail.com)"}

def search_wikidata_entity(tag):
    """
    Busca la entidad más relevante en Wikidata para una tag dada.
    Retorna QID, label y descripción si encuentra, sino None.
    """
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "es",
        "search": tag
    }
    response = requests.get(url, params=params, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if data.get("search"):
            entity = data["search"][0]
            return entity["id"], entity["label"], entity.get("description", "")
    return None, None, None

# Leer tags del CSV generado por main.py
input_csv = "tags.csv"
df = pd.read_csv(input_csv)

# Eliminar duplicados para no consultar lo mismo varias veces
unique_tags = df["Título 1"].drop_duplicates().tolist()


# Concurrencia para acelerar la comparación
def process_tag(tag):
    qid, label, description = search_wikidata_entity(tag)
    return {
        "tag": tag,
        "wikidata_qid": qid,
        "wikidata_label": label,
        "wikidata_description": description
    }

results = []
max_workers = 12  # Puedes ajustar este valor según tu conexión
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(process_tag, tag): tag for tag in unique_tags}
    for f in tqdm(as_completed(futures), total=len(futures), desc="Comparando con Wikidata (concurrente)"):
        try:
            results.append(f.result())
        except Exception as e:
            print(f"Error con tag '{futures[f]}': {e}")

# Guardar resultados
output_csv = "tags_wikidata_comparison.csv"
pd.DataFrame(results).to_csv(output_csv, index=False)
print(f"Comparación guardada en {output_csv}")
