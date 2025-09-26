# Entities Extract

Una herramienta para extraer entidades y compararlas con Wikidata a partir de sitemaps XML.

## Descripción

Este proyecto permite:
- Extraer URLs de artículos desde sitemaps XML
- Extraer títulos/encabezados de páginas web
- Comparar términos extraídos con entidades de Wikidata
- Generar reportes en formato CSV

## Requisitos

- Python 3.8 o superior
- UV (gestor de paquetes Python rápido)

## Instalación

1. Clonar o descargar el repositorio:
   ```bash
   git clone https://github.com/pichu2707/entities-extract.git
   cd entities-extract
   ```

2. Instalar dependencias con UV:
   ```bash
   uv sync
   ```

## Uso

### 1. Extraer datos principales

El script principal extrae datos de un sitemap y genera un CSV con URLs y títulos:

```bash
uv run main.py
```

**Configuración personalizable:**
- Modifica `sitemap_url` en `main.py` para usar otro sitemap
- Ajusta `N_HEADS_PRUEBA` para cambiar el número de páginas a procesar (por defecto: 20 para pruebas)
- Cambia `max_workers` en ThreadPoolExecutor para ajustar la velocidad de procesamiento

### 2. Comparar con Wikidata (opcional)

Para comparar los términos extraídos con entidades de Wikidata:

```bash
uv run compared_entities.py
```

Este script:
- Lee el CSV generado por `main.py`
- Busca cada término en la API de Wikidata
- Genera un nuevo CSV con las coincidencias encontradas

## Archivos generados

- `urls_heads.csv`: URLs y títulos extraídos del sitemap
- `tags_wikidata_comparison.csv`: Comparación con entidades de Wikidata

## Configuración avanzada

### Procesamiento completo vs. pruebas

Por defecto, el script está configurado para procesar solo 20 elementos para pruebas rápidas. Para procesar todo el dataset:

1. En `main.py`, cambia o elimina la línea:
   ```python
   N_HEADS_PRUEBA = 20  # Elimina esta limitación
   article_urls_prueba = article_urls[:N_HEADS_PRUEBA]  # Usa article_urls completo
   ```

### Ajustar concurrencia

- En `main.py`: Modifica `max_workers=16` según tu CPU/conexión
- En `compared_entities.py`: Modifica `max_workers=12` para las consultas a Wikidata

### User-Agent personalizado

Para las consultas a Wikidata, personaliza el User-Agent en `compared_entities.py`:

```python
HEADERS = {"User-Agent": "tu-proyecto/1.0 (tu_email@dominio.com)"}
```

## Estructura del proyecto

```
entities-extract/
├── main.py                    # Script principal
├── extract_sitemap.py         # Funciones de extracción
├── compared_entities.py       # Comparación con Wikidata
├── wikidata_test.py          # Script de pruebas para Wikidata API
├── requirements.txt           # Dependencias
├── pyproject.toml            # Configuración del proyecto
└── README.md                 # Este archivo
```

### Script de pruebas (wikidata_test.py)

El archivo `wikidata_test.py` es una herramienta de desarrollo para:

- **Probar la API de Wikidata**: Verifica que las consultas funcionen correctamente
- **Depurar problemas**: Muestra la URL de petición, código HTTP y respuesta JSON completa
- **Validar términos específicos**: Permite probar búsquedas individuales antes del procesamiento masivo

**Uso:**
```bash
uv run wikidata_test.py
```

Este script es especialmente útil si `compared_entities.py` no devuelve resultados esperados, ya que permite diagnosticar problemas de conectividad, User-Agent, o formato de respuesta de la API.

## Dependencias principales

- `pandas`: Manipulación de datos y CSV
- `requests`: Peticiones HTTP
- `beautifulsoup4`: Parsing de HTML/XML
- `tqdm`: Barras de progreso
- `lxml`: Parser XML (opcional, mejora rendimiento)

## Troubleshooting

### Error 403 en Wikidata
Si ves un error "Please set a user-agent", asegúrate de que el User-Agent esté configurado correctamente en `compared_entities.py`.

### Proceso muy lento
- Reduce `max_workers` si tienes problemas de conexión
- Usa `N_HEADS_PRUEBA` para probar con menos datos primero

### Sin resultados en Wikidata
- Verifica que los términos estén limpios (sin "Archives" u otros sufijos)
- Prueba con términos más específicos o en singular

## Contribuir

1. Fork del repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request

## Mejoras

Si tienes alguna mejora pensada puedes mandármelo a [mi correo](mailto:hola@javilazaro.es)


## Licencia

MIT License - ver archivo LICENSE para detalles.

