import requests
import os
import time
import matplotlib.pyplot as plt
import numpy as np

# Cargar el token de solo lectura para acceder a repos privados
GITHUB_TOKEN = os.getenv("PAT_GITHUB_PRIVATE")

if not GITHUB_TOKEN:
    print("❌ Error: la variable de entorno PAT_GITHUB_PRIVATE no está definida. Configúrala antes de ejecutar este script.")
    exit(1)
USERNAME = "ipatzantzic19"  # Reemplaza con tu nombre de usuario de GitHub

# Configurar la cabecera de autenticación para GitHub API
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Obtener lista de repositorios (incluyendo privados)
repos_url = "https://api.github.com/user/repos?per_page=100&visibility=all"
repos = requests.get(repos_url, headers=headers).json()

# Diccionario para contar bytes por lenguaje
language_stats = {}

for repo in repos:
    languages_url = repo.get("languages_url", "")
    if languages_url:
        languages_data = requests.get(languages_url, headers=headers).json()
        for lang, bytes_used in languages_data.items():
            language_stats[lang] = language_stats.get(lang, 0) + bytes_used

# Calcular porcentaje de uso
total_bytes = sum(language_stats.values())
language_percentages = {
    lang: round((bytes_used / total_bytes) * 100, 4)
    for lang, bytes_used in language_stats.items()
}

# Ordenar de mayor a menor
sorted_languages = sorted(language_percentages.items(), key=lambda x: x[1], reverse=True)

#---------------------------------------------
def generate_language_chart(data):
    languages = [lang for lang, _ in data]
    percentages = [percent for _, percent in data]

    fig, ax = plt.subplots(figsize=(10, 6))
    y_pos = np.arange(len(languages))

    # Colores personalizados
    colors = plt.cm.viridis(np.linspace(0.2, 1, len(languages)))

    ax.barh(y_pos, percentages, color=colors, align="center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(languages)
    ax.invert_yaxis()
    ax.set_xlabel("Porcentaje de Uso (%)")

    for i, v in enumerate(percentages):
        ax.text(v + 1, i, f"{v}%", va="center", fontsize=10)

    # Guardar la imagen
    plt.savefig("scripts/languages.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print("✅ Imagen `languages.png` generada correctamente.")

"""Script para generar una imagen de lenguajes usados.

Genera scripts/languages.png a partir de la API de GitHub,
pero ya no modifica el README.md. La sección del README
se gestiona manualmente.
"""

# Generar la imagen si hay datos
if sorted_languages:
    generate_language_chart(sorted_languages)
#---------------------------------------------