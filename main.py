import pandas as pd
from tqdm import tqdm

# Optimización: extracción concurrente de heads
from concurrent.futures import ThreadPoolExecutor, as_completed

from extract_sitemap import (
    extract_sitemap_urls, 
    extract_article_urls, 
    extract_tags, 
    extract_head,
    )

sitemap_url = "https://news.bitcoin.com/sitemap.xml"
tag_urls = extract_sitemap_urls(sitemap_url)


# Progreso al extraer URLs de artículos
article_urls = []
for tag_url in tqdm(tag_urls, desc="Extrayendo artículos", unit="tag"):
    article_urls.extend(extract_article_urls([tag_url]))

# Progreso al extraer etiquetas
tags = []
for article_url in tqdm(article_urls, desc="Extrayendo tags", unit="artículo"):
    tags.append(extract_tags([article_url]))



def extract_head_single(url):
    # Suponiendo que extract_head espera una lista, pero solo le pasamos un artículo
    return extract_head([url])

heads = []
with ThreadPoolExecutor(max_workers=16) as executor:  # Puedes ajustar max_workers según tu CPU/conexión
    futures = {executor.submit(extract_head_single, url): url for url in article_urls}
    for f in tqdm(as_completed(futures), total=len(futures), desc="Extrayendo heads (concurrente)", unit="artículo"):
        try:
            heads.append(f.result())
        except Exception as e:
            print(f"Error extrayendo head: {e}")



def urls_heads_to_csv(urls: list[str], heads: list, filename: str = "urls_heads.csv") -> pd.DataFrame:
    """
    Guarda las URLs y los heads alineados en un archivo CSV.
    """
    # Aplanar heads si es lista de listas o lista de un solo string
    flat_heads = [item[0] if isinstance(item, list) and item else (item if item else "") for item in heads]
    min_len = min(len(urls), len(flat_heads))
    df = pd.DataFrame({
        'url': urls[:min_len],
        'head': flat_heads[:min_len]
    })
    df.to_csv(filename, index=False)
    print(f"CSV creado: {filename}")
    return df

# Guardar las urls y heads en un CSV
urls_heads_to_csv(tags, heads)