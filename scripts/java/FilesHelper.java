import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Utilitário simples para leitura de arquivos de recursos. */
public final class FilesHelper {
    private FilesHelper() {}

    public static String readResource(String relativePath) throws IOException {
        return Files.readString(Path.of(relativePath), StandardCharsets.UTF_8);
    }
}
