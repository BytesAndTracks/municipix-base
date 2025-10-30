"""Assina XML NFSe utilizando certificado A1 em formato PKCS#12."""

from pathlib import Path
from signxml import XMLSigner  # type: ignore
from lxml import etree
from OpenSSL.crypto import load_pkcs12  # type: ignore

CERT_PATH = Path("./certs/municipix.pfx")
CERT_PASSWORD = "trocar"
XML_PATH = Path("../../examples/abrasf_enviar_rps.xml")
OUTPUT_PATH = Path("../../examples/abrasf_enviar_rps_assinado.xml")


def load_credentials():
    pkcs12 = load_pkcs12(CERT_PATH.read_bytes(), CERT_PASSWORD.encode())
    return pkcs12.get_certificate(), pkcs12.get_privatekey(), pkcs12.get_ca_certificates()


def sign_xml(xml_path: Path, output_path: Path) -> None:
    cert, key, cas = load_credentials()
    data = xml_path.read_bytes()
    document = etree.fromstring(data)
    signer = XMLSigner(method=XMLSigner.RSA_SHA256, c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315")
    signed_root = signer.sign(document, key=key, cert=cert, ca_store=cas)
    output_path.write_bytes(etree.tostring(signed_root, encoding="utf-8", xml_declaration=True))


if __name__ == "__main__":
    sign_xml(XML_PATH, OUTPUT_PATH)
    print(f"Arquivo assinado salvo em {OUTPUT_PATH}")
