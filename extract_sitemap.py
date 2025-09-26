import urllib
import requests
from bs4 import BeautifulSoup
import re

def extract_sitemap_urls(sitemap_url: str)->list[str]:
    """
    Extraer las URLs de un sitemap XML.
    """
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    tag_urls = [loc.text for loc in soup.find_all('loc') if 'tag' in loc.text]
    return tag_urls

def extract_article_urls(tag_url: list[str])->list[str]:
    """
    Extraer las URLs de los artículos de una lista de páginas de etiquetas.
    tag_urls puede ser una lista de URLs de etiquetas.
    """
    article_urls = []
    for url in tag_url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        # Extraer todas las URLs de artículos dentro de cada sitemap de etiqueta
        urls = [loc.text for loc in soup.find_all('loc') if re.match(r'https://news\.bitcoin\.com/[a-zA-Z0-9-]+', loc.text)]
        article_urls.extend(urls)
    return article_urls

def extract_tags(article_urls: list[str])->list[str]:
    """
    Extraer las etiquetas de una lista de URLs de artículos.
    """
    tags = []
    for url in article_urls:
        tag = re.findall(r'https:\/\/news\.bitcoin\.com\/tag\/([a-zA-Z0-9-]+)', url)
        tags.append(tag)
    return tags

def extract_head(article_urls: list[str])->list[str]:
    """
    Extraer los títulos de una lista de URLs de artículos.
    """
    heads = []
    for url in article_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        head = soup.find('h2', class_='entry-title').text if soup.find('h1', class_='entry-title') else 'No title found'
        heads.append(head)
    return heads