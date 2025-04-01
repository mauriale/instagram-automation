# Instagram Automation Project

## Descripción
Este proyecto automatiza la creación de imágenes y descripciones usando IA, y publica contenido diariamente en Instagram.

## Instalación
1. Clona el repositorio: `git clone <URL>`
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tus claves en `config/config.json`.

## Uso
Ejecuta el script principal:

```bash
python src/main.py
```

Para ejecutar en modo programado (publicación diaria automática):

```bash
python src/main.py --mode scheduled
```

## Características
- Generación de imágenes usando Hugging Face
- Creación de descripciones atractivas con Claude
- Publicación automática en Instagram
- Programación de publicaciones recurrentes

## Configuración
Edita el archivo `config/config.json` para personalizar:
- Claves API de Hugging Face e Instagram
- Estilo de las imágenes generadas
- Frecuencia de publicación
- Hashtags predeterminados

## Requisitos
- Python 3.8+
- Cuenta en Hugging Face con API key
- Cuenta de desarrollador de Facebook/Instagram con permisos adecuados