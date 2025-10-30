import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.file.Path;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.X509Certificate;

import javax.xml.parsers.DocumentBuilderFactory;

import org.apache.xml.security.Init;
import org.apache.xml.security.signature.XMLSignature;
import org.apache.xml.security.transforms.Transforms;
import org.apache.xml.security.utils.Constants;
import org.apache.xml.security.utils.XMLUtils;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

/**
 * Assinatura XML utilizando XMLDSig (Apache Santuario).
 */
public class XmlSigner {
    private static final Path SOURCE_XML = Path.of("../../examples/abrasf_enviar_rps.xml");
    private static final Path OUTPUT_XML = Path.of("../../examples/abrasf_enviar_rps_signed.xml");
    private static final Path CERTIFICATE = Path.of("./certs/municipix.pfx");
    private static final char[] PASSWORD = "trocar".toCharArray();

    static {
        Init.init();
    }

    public static void main(String[] args) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setNamespaceAware(true);
        Document document = dbf.newDocumentBuilder().parse(SOURCE_XML.toFile());

        KeyStore keyStore = KeyStore.getInstance("PKCS12");
        keyStore.load(new FileInputStream(CERTIFICATE.toFile()), PASSWORD);

        String alias = keyStore.aliases().nextElement();
        PrivateKey privateKey = (PrivateKey) keyStore.getKey(alias, PASSWORD);
        X509Certificate certificate = (X509Certificate) keyStore.getCertificate(alias);

        XMLSignature signature = new XMLSignature(document, SOURCE_XML.toString(), XMLSignature.ALGO_ID_SIGNATURE_RSA_SHA256);
        Element root = document.getDocumentElement();
        root.appendChild(signature.getElement());

        Transforms transforms = new Transforms(document);
        transforms.addTransform(Transforms.TRANSFORM_ENVELOPED_SIGNATURE);
        transforms.addTransform(Transforms.TRANSFORM_C14N_EXCL_OMIT_COMMENTS);
        signature.addDocument("", transforms, Constants.ALGO_ID_DIGEST_SHA256);

        signature.addKeyInfo(certificate);
        signature.addKeyInfo(certificate.getPublicKey());

        signature.sign(privateKey);

        try (FileOutputStream fos = new FileOutputStream(OUTPUT_XML.toFile())) {
            XMLUtils.outputDOM(document, fos);
        }
    }
}
