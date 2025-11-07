# MUNICIPIX Knowledge Base 🧩
Base de conhecimento técnica para integrações NFSe municipais brasileiras.

## Estrutura
- `/docs` → Manuais e normas (ABRASF, IPM, Thema, etc.)
- `/schemas` → Schemas XSD organizados por provedor
- `/wsdl` → Arquivos WSDL das prefeituras
- `/examples` → XMLs e envelopes SOAP válidos
- `/scripts` → Exemplos de integração (Python e Java)

## Fonte Original
Adaptado a partir do projeto [ACBr](https://github.com/frones/ACBr).

## Uso
Repositório utilizado pelo agente **MUNICIPIX** para análise, geração e validação de integrações NFSe.

### 📦 Últimas atualizações — 2025-10-29
- Adicionado: WSDL São Leopoldo-RS (consulta e remessa Thema)
- Adicionado: WSDL São José dos Pinhais-PR (issOnline2)
- Falhou: WSDL Canela-RS (erro de TLS na conexão)
- Falhou: WSDL Gramado-RS (retorno 401 Acesso Negado)
- Falhou: WSDL Novo Hamburgo-RS (retorno 401 Acesso Negado)
