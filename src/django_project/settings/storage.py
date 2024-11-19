import os.path

STATIC_URL = config["storage"]["static_url"]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = config["storage"]["media_url"]
MEDIA_ROOT = config["storage"]["media_root"]
