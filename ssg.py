def main():
    import os
    import markdown
    import yaml
    from jinja2 import Environment, PackageLoader, select_autoescape

    env = Environment(loader=PackageLoader("templates"), autoescape=select_autoescape())
    template = env.get_template("basic.html")

    def parse_mardown(md_bestand):
        bestand = open(
            md_bestand, "r"
        )  # Je opent het markdown bestand en zet het in een varianbele
        content = (
            bestand.read()
        )  # Je leest heel het open markdown bestand in en zet dit ook in een variabele
        delen = content.split("---\n", 1)  # Split de tekst op de eerste "---\n"
        front_matter = delen[0]  # Eerste deel (YAML metadata)
        markdown_body = delen[1]  # Tweede deel (Markdown-tekst)
        try:
            yaml_data = yaml.safe_load(
                front_matter
            )  # Dit zet de YAML om in een python dictionary, de Yaml sleutels worden de dictionary sleutels: bron(https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python)
        except:
            print("er is een fout opgetreden met het YAML bestand")
        return yaml_data, markdown_body


if __name__ == "__main__":
    main()
