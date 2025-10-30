# MUNICIPIX Agent Playbook

## Core Layout
- `setup_municipix_repo.py` sincroniza `acbr_clone/`; execute `python setup_municipix_repo.py` antes de buscar novos schemas; nunca commite `acbr_clone/`.
- `schemas/` guarda XSD organizados por provedor: exemplo `schemas/ginfes/1.00/servico_enviar_lote_rps_envio_v03.xsd`; mantenha a convenção `<provedor>/<versao>/<arquivo>.xsd`.
- `examples/` armazena XML de referência (ABRASF, GINFES, Betha, SystemPro/Canela); mantenha dados fictícios e bem indentados porque os scripts de assinatura/validação leem esses arquivos diretamente.
- `wsdl/` contém subpastas por município; armazene aqui contratos `.wsdl` originais e atualize `wsdl/README.md` com notas de versão quando novos arquivos forem adicionados.
- `docs/` lista os manuais oficiais necessários; substitua os placeholders por PDFs reais assim que disponíveis e registre a origem no `docs/README.md`.

## Atualização de Artefatos
- Sempre rode `python setup_municipix_repo.py` para clonar/atualizar o ACBr antes de copiar novos schemas ou exemplos.
- Para copiar schemas NFSe do ACBr, utilize `Copy-Item`/`robocopy` preservando a hierarquia original e adicione apenas provedores relevantes (ex.: `PadraoNacional` → `schemas/abrasf`).
- Quando criar novos XMLs de exemplo, derive a estrutura dos arquivos em `acbr_clone/Testes/Recursos/NFSe/Provedores/` e atualize os campos (`CodigoMunicipio`, `ItemListaServico`) conforme a prefeitura alvo.

## Scripts Python
- Dependências: instale com `pip install requests pyopenssl signxml lxml`.
- `scripts/python/send_nfse.py` assume certificado A1 em `./certs/municipix.pfx`; o helper `load_pkcs12` gera PEM temporários. Ajuste `WSDL_URL`, `SOAP_ACTION` e payload apontando para `examples/`.
- `scripts/python/sign_xml.py` usa SignXML para assinar; altere `XML_PATH`, `CERT_PATH` e garanta que o documento possua `Id` na tag alvo.
- `scripts/python/validate_xml.py` valida usando `lxml.etree.XMLSchema`; atualize `SCHEMA_PATH` para a versão correta antes de rodar.

## Scripts Java
- Projetos Java requerem Apache Santuario (`xmlsec`) no classpath. Compile com `javac -cp lib/xmlsec-3.0.2.jar;. scripts/java/*.java` e rode com `java -cp lib/xmlsec-3.0.2.jar;. SoapSender`.
- `SoapSender.java` lê XMLs relativos a `examples/`; mantenha os caminhos estáveis ao mover arquivos.
- `XmlSigner.java` carrega certificados PKCS12 (arquivo .pfx); confirme a presença de `certs/municipix.pfx` e das libs `xmlsec` antes de executar.

## Contribuição
- Preserve UTF-8 sem BOM em XML e evite tabulações; use dois espaços para indentação em exemplos.
- Inclua changelog sucinto nos README correspondentes sempre que inserir novas versões de schemas/WSDLs.
- Antes de concluir, valide qualquer XML atualizado com `validate_xml.py` e mantenha uma cópia assinada opcionalmente em `examples/*_signed.xml`.
- Para novos provedores, crie estrutura mínima `schemas/<provedor>/<versao>/`, `wsdl/<municipio>/` e adicione exemplos + scripts mencionando o provedor.
