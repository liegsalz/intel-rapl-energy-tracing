import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.net.InetSocketAddress;

public class Main {
    public static void main(String[] args) throws IOException {
        var server = HttpServer.create(new InetSocketAddress(8080), 0);

        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                var filePath = "../index.html";

                byte[] response;
                try {
                    response = Files.readAllBytes(Paths.get(filePath));
                    exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                    exchange.sendResponseHeaders(200, response.length);
                    var os = exchange.getResponseBody();
                    os.write(response);
                    os.close();
                } catch (IOException e) {
                    // If the file is not found, send a 404 response
                    String errorMessage = "404 (Not Found)\n";
                    exchange.sendResponseHeaders(404, errorMessage.length());
                    OutputStream os = exchange.getResponseBody();
                    os.write(errorMessage.getBytes());
                    os.close();
                }
            }
        });

        server.start();
    }
}
