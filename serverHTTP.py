from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

# Classe para manipular as requisições do servidor
class CustomHandler(SimpleHTTPRequestHandler):
    # Diretório a ser listado
    directory = '/home/USER'  # Altere para o diretório desejado

    # Método para listar os arquivos do diretório
    def list_directory(self, path):
        try:
            list_dir = os.listdir(path)
            body = '<h2>Arquivos:</h2><ul>'
            for file in list_dir:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    body += f'<li><a href="{file}">{file}</a></li>'
            body += '</ul>'
            return body
        except OSError:
            self.send_error(404, "Erro ao acessar o diretório")

    # Método para retornar o cabeçalho HTTP da requisição especial /HEADER
    def do_SPECIAL_PATH(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(self.headers.as_string().encode('utf-8'))

    # Sobrescrever a função que lida com requisições GET
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Se a requisição for para o caminho especial /HEADER
        if parsed_path.path == '/HEADER':
            self.do_SPECIAL_PATH()
            return

        # Se a requisição for para um arquivo específico
        if parsed_path.path != '/' and os.path.isfile(os.path.join(self.directory, parsed_path.path[1:])):
            return SimpleHTTPRequestHandler.do_GET(self)

        # Se a requisição for para listar os arquivos do diretório
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(self.list_directory(self.directory).encode('utf-8'))

port = int(input("Digite a porta de conexão: "))

if __name__ == '__main__':
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, CustomHandler)
        print(f'Servidor rodando na porta {port}...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C Recebido, encerrando o servidor...')
        httpd.socket.close()
