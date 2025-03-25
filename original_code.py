import os
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Jinja2-omgeving instellen met automatische escaping voor veiligheid
# Bron: https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment
env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
template = env.get_template("basic.html")


def parse_markdown(md_bestand):
    bestand = open(
        md_bestand, "r"
    )  # Je opent het markdown bestand en zet het in een variabele
    content = (
        bestand.read()
    )  # Je leest heel het open markdown bestand in en zet dit ook in een variabele
    delen = content.split("---\n", 2)  # Split de tekst op de eerste "---\n"
    front_matter = delen[1].strip()  # Eerste deel (YAML metadata)
    markdown_body = delen[2]  # Tweede deel (Markdown-tekst)

    try:
        yaml_data = yaml.safe_load(
            front_matter
        )  # Zet de YAML om in een Python dictionary
        # Bron: https://pyyaml.org/wiki/PyYAMLDocumentation
    except:
        print("Er is een fout opgetreden met het YAML bestand")

    return yaml_data, markdown_body


def site_generator():
    for folder in [
        "pages",
        "posts",
    ]:  # Loopt door de lijst zodat statische pagina's en blogposts verwerkt worden.
        # Bron: https://www.geeksforgeeks.org/python-loop-through-folders-and-files-in-directory/
        for files in os.listdir(
            folder
        ):  # Haalt een lijst op van alle bestanden in de huidige folder.
            if files.endswith(".md"):  # Controleert of een bestand eindigt op .md
                md_files = os.path.join(folder, files)  # Maakt een pad naar het bestand
                yaml_data, markdown_body = parse_markdown(
                    md_files
                )  # Gebruikt vorige functie om de YAML en Markdown te parsen.
                layout = yaml_data.get(
                    "layout"
                )  # Haalt de layout op uit het YAML-bestand.
                template = env.get_template(
                    layout
                )  # Laadt het basis Jinja-template in.
                # Bron: https://jinja.palletsprojects.com/en/3.0.x/templates/#

                html_content = markdown.markdown(
                    markdown_body
                )  # Zet Markdown om naar HTML
                # Bron: https://python-markdown.github.io/

                volledige_pagina = template.render(
                    yaml_data, content=html_content
                )  # Render de HTML-pagina met Jinja2

                output_folder = "_site"  # Output directory voor gegenereerde bestanden
                os.makedirs(
                    output_folder, exist_ok=True
                )  # Maak directory aan indien deze niet bestaat
                output_path = os.path.join(
                    output_folder, files.replace(".md", ".html")
                )  # Zet de extensie om naar .html

                output_file = open(
                    output_path, "w"
                )  # Open het outputbestand in schrijfmodus
                output_file.write(
                    volledige_pagina
                )  # Schrijf de gegenereerde HTML naar het bestand
                print(f"Gegenereerd: {output_path}")  # Geef een melding in de terminal


if __name__ == "__main__":
    site_generator()
