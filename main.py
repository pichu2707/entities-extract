import pandas as pd

from extract_sitemap import (
    extract_sitemap_urls, 
    extract_article_urls, 
    extract_tags, 
    extract_head,
    )

sitemap_url = "https://www.tudominio.com/sitemap.xml"
tag_urls = extract_sitemap_urls(sitemap_url)
article_urls = extract_article_urls(tag_urls)
tags = extract_tags(article_urls)
heads = extract_head(article_urls)


def tags_to_csv(tags: list[str], heads: list[str], filename: str="tags.csv")->pd.DataFrame:
    """
    Guardar las etiquetas en un archivo CSV.
    """
    flat_tags = [item for sublist in tags for item in sublist]
    flat_heads = [head for sublist in heads for head in sublist]
    df = pd.DataFrame({'tag': flat_tags, 'head': flat_heads})
    df.to_csv(filename, index=False)
    print(f"CSV creado: {filename}")
    return df

# Guardar las etiquetas en un CSV
tags_to_csv(tags)