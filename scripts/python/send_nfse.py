"""Envio de lote NFSe utilizando SOAP 1.1 com autenticação por certificado."""

from pathlib import Path
from typing import Tuple
import ssl
import requests

# Ajuste as constantes conforme o provedor alvo
WSDL_URL = "https://homologacao.canela.rs.gov.br/nfse/services/NfseWS?wsdl"
SOAP_ACTION = "EnviarLoteRps"
CERT_PATH = Path("./certs/municipix.pfx")
CERT_PASSWORD = "trocar"

SOAP_TEMPLATE = """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">
  <s:Body>
    {payload}
  </s:Body>
</s:Envelope>
"""


def load_pkcs12(pfx_path: Path, password: str) -> Tuple[str, str]:
    """Extrai caminhos temporários para chave e certificado a partir de um .pfx."""
    from OpenSSL.crypto import load_pkcs12, dump_privatekey, dump_certificate, FILETYPE_PEM  # type: ignore

    pfx = load_pkcs12(pfx_path.read_bytes(), password.encode())
    private_key = dump_privatekey(FILETYPE_PEM, pfx.get_privatekey())
    certificate = dump_certificate(FILETYPE_PEM, pfx.get_certificate())

    key_file = pfx_path.with_suffix(".key.pem")
    crt_file = pfx_path.with_suffix(".crt.pem")
    key_file.write_bytes(private_key)
    crt_file.write_bytes(certificate)
    return str(crt_file), str(key_file)


def send_payload(payload_xml: str) -> requests.Response:
    """Assina o payload com certificado A1 e dispara a requisição SOAP."""
    crt_file, key_file = load_pkcs12(CERT_PATH, CERT_PASSWORD)

    envelope = SOAP_TEMPLATE.format(payload=payload_xml)
    response = requests.post(
        WSDL_URL.replace("?wsdl", ""),
        data=envelope.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": SOAP_ACTION,
        },
        cert=(crt_file, key_file),
        verify=True,
        timeout=30,
    )
    response.raise_for_status()
    return response


if __name__ == "__main__":
    payload = Path("../../examples/canela_enviar_lote_rps.xml").read_text(encoding="utf-8")
    result = send_payload(payload)
    print("Status:", result.status_code)
    print(result.text)
