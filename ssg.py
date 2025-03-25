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
    """
    Deze functie genereert een statische website uit Markdown-bestanden.
    Het leest YAML-front-matter voor metadata en zet de inhoud om naar HTML.
    Ook maakt het een navigatiemenu op basis van pagina's met 'menu: true'.
    """

    navigatie = []  # Lijst waarin de links voor de navigatiebalk worden opgeslagen

    # Eerste loop: Verzamel alle pagina's die in de navigatiebalk moeten komen
    for folder in ["pages", "posts"]:  # Doorloopt beide mappen met inhoud
        for files in os.listdir(
            folder
        ):  # Haalt een lijst op van alle bestanden in de map
            if files.endswith(
                ".md"
            ):  # Controleert of het bestand een Markdown-bestand is
                md_files = os.path.join(folder, files)  # Pad naar het bestand opbouwen
                yaml_data, markdown_body = parse_markdown(
                    md_files
                )  # Haalt metadata en content op

                # Als het 'menu' attribuut in de front-matter staat, voeg het toe aan de navigatie
                if yaml_data.get("menu"):
                    navigatie.append(
                        {
                            "title": yaml_data["title"],  # Titel van de pagina
                            "url": files.replace(
                                ".md", ".html"
                            ),  # Verander bestandsnaam naar .html
                        }
                    )

    # Tweede loop: Genereer de HTML-pagina’s en voeg de navigatie toe
    for folder in ["pages", "posts"]:
        for files in os.listdir(folder):
            if files.endswith(".md"):
                md_files = os.path.join(folder, files)
                yaml_data, markdown_body = parse_markdown(
                    md_files
                )  # Markdown en YAML verwerken
                layout = yaml_data.get("layout")  # Welke template wordt gebruikt?
                template = env.get_template(layout)  # Laad de juiste Jinja2-template

                html_content = markdown.markdown(
                    markdown_body
                )  # Zet Markdown om naar HTML
                volledige_pagina = template.render(
                    yaml_data, content=html_content, navigation=navigatie
                )  # Vul de template met de inhoud en navigatie

                output_folder = (
                    "_site"  # Map waarin de gegenereerde bestanden worden opgeslagen
                )
                os.makedirs(
                    output_folder, exist_ok=True
                )  # Maak de map aan als die niet bestaat
                output_path = os.path.join(
                    output_folder, files.replace(".md", ".html")
                )  # Output-bestandspad

                # Schrijf de HTML naar een bestand
                with open(output_path, "w") as output_file:
                    output_file.write(volledige_pagina)

                print(f"Gegenereerd: {output_path}")  # Bevestiging in de terminal


if __name__ == "__main__":
    site_generator()
