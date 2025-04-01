# Instagram Automation Project

## Descripción
Este proyecto automatiza la creación de imágenes y descripciones usando IA, y publica contenido diariamente en Instagram.

## Instalación
1. Clona el repositorio: 
   ```bash
   git clone https://github.com/mauriale/instagram-automation.git
   cd instagram-automation
   ```

2. Instala las dependencias: 
   ```bash
   pip install -r requirements.txt
   ```

3. Configura tus claves API:
   - Copia `.env.example` a `.env` y añade tus claves API
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus claves API
   ```

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
- Estilo de las imágenes generadas
- Frecuencia de publicación
- Hashtags predeterminados

## API Keys Necesarias
- Hugging Face API Key: Para generación de imágenes
- Anthropic API Key: Para generar descripciones con Claude
- Instagram Graph API: Para publicar automáticamente

## Requisitos
- Python 3.8+
- Cuenta en Hugging Face con API key
- Cuenta de desarrollador de Facebook/Instagram con permisos adecuados