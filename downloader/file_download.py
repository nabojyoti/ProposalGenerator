import tempfile
import requests


def html_downloader(page_url: str):
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(response.text)
            return temp_file.name
    except requests.exceptions.RequestException as e:
        print(f"Error downloading HTML: {e}")
        return None
