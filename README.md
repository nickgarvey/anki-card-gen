# Anki Card Generator

Simple tool to generate a file suitable for Anki Text Import.

Uses OpenAI gpt-4o to generate the cards.

`secrets/openai_api_key.txt` should contain your API key for the query.

## Usage
```
python3 -m venv .env
source .env/bin/activate
pip install poetry
poetry install
anki-card-gen
```
