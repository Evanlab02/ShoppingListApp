"""Contains github api call functions."""

import requests

OWNER = "Evanlab02"
APP_REPO = "ShoppingListApp"
FRONT_END_REPO = "ShoppingListApp-FE"
BACK_END_REPO = "ShoppingListApp-BE"


def download_app_release():
    """Download the app release from github."""
    url = f"https://api.github.com/repos/{OWNER}/{APP_REPO}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    assets = data.get("assets")
    download_url = asset[0].get("browser_download_url")
    for asset in assets:
        if asset.get("name") == "app.zip":
            download_url = asset.get("browser_download_url")
            break
    response = requests.get(download_url)
    response.raise_for_status()
    with open("app.zip", "wb") as f:
        f.write(response.content)


def download_frontend_release():
    """Download the frontend release from github."""
    url = f"https://api.github.com/repos/{OWNER}/{FRONT_END_REPO}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    assets = data.get("assets")
    asset = assets[0]
    download_url = asset.get("browser_download_url")
    response = requests.get(download_url)
    response.raise_for_status()
    with open("frontend.zip", "wb") as f:
        f.write(response.content)


def download_backend_release():
    """Download the backend release from github."""
    url = f"https://api.github.com/repos/{OWNER}/{BACK_END_REPO}/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    assets = data.get("assets")
    asset = assets[0]
    download_url = asset.get("browser_download_url")
    response = requests.get(download_url)
    response.raise_for_status()
    with open("backend.zip", "wb") as f:
        f.write(response.content)
