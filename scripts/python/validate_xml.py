"""Valida XML NFSe contra um schema XSD específico."""

from pathlib import Path
from lxml import etree

XML_PATH = Path("../../examples/ginfes_consultar_nfse.xml")
SCHEMA_PATH = Path("../../schemas/ginfes/1.00/servico_consultar_nfse_envio_v03.xsd")


def validate(xml_path: Path, schema_path: Path) -> None:
    xml_doc = etree.parse(str(xml_path))
    schema_doc = etree.parse(str(schema_path))
    schema = etree.XMLSchema(schema_doc)
    schema.assertValid(xml_doc)


if __name__ == "__main__":
    try:
        validate(XML_PATH, SCHEMA_PATH)
        print("XML válido contra o schema informado.")
    except (etree.DocumentInvalid, FileNotFoundError) as exc:
        print(f"Validação falhou: {exc}")
