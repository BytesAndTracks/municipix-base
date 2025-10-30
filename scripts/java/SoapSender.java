import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

/**
 * Envia envelopes SOAP para provedores NFSe que seguem o padrão ABRASF.
 */
public class SoapSender {
    private static final String SERVICE_URL = "https://homologacao.ginfes.com.br/nfse/services/NfseService";
    private static final String SOAP_ACTION = "ConsultarNfse";

    public static void main(String[] args) throws IOException {
        String payload = FilesHelper.readResource("../../examples/ginfes_consultar_nfse.xml");
        String envelope = buildEnvelope(payload);

        HttpURLConnection connection = (HttpURLConnection) new URL(SERVICE_URL).openConnection();
        connection.setRequestMethod("POST");
        connection.setDoOutput(true);
        connection.setRequestProperty("Content-Type", "text/xml; charset=utf-8");
        connection.setRequestProperty("SOAPAction", SOAP_ACTION);

        try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(connection.getOutputStream(), StandardCharsets.UTF_8))) {
            writer.write(envelope);
        }

        int status = connection.getResponseCode();
        System.out.println("HTTP Status: " + status);

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
            reader.lines().forEach(System.out::println);
        }
    }

    private static String buildEnvelope(String payload) {
        return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" +
                "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">" +
                "<soapenv:Header/>" +
                "<soapenv:Body>" + payload + "</soapenv:Body>" +
                "</soapenv:Envelope>";
    }
}
