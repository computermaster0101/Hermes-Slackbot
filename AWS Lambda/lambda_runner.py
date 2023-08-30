import http.server
import socketserver
import socket
import json
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from lambda_function import lambda_handler



def lambda_runner(lambda_function):
    class LocalLambdaHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.respond('GET')

        def do_POST(self):
            self.respond('POST')

        def respond(self, http_method):
            if self.path == '/favicon.ico':
                self.send_response(HTTPStatus.OK)
                return

            parsed_url = urlparse(self.path)
            query_params = {key: value[0] for key, value in parse_qs(parsed_url.query).items()}

            content_length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(content_length)

            event = {
                "httpMethod": http_method,
                "queryStringParameters": query_params,
                "path": parsed_url.path,
                "headers": dict(self.headers),
                "isBase64Encoded": False
            }

            try:
                content_type = self.headers.get('Content-Type', '')
                if 'encoded' in content_type:
                    decoded_body = body.decode('utf-8')
                    event["body"] = decoded_body
                    print("decoded encoded body")
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-type', 'application/json')
                    response = 'OK'
                    response_bytes = response.encode('utf-8')
                    self.send_header('Content-Length', len(response_bytes))
                    self.end_headers()
                    self.wfile.write(response_bytes)
                else:
                    event["body"] = body
                    print("body not encoded")
            except UnicodeDecodeError:
                event["body"] = body
                print("defaulting body because of UnicodeDecodeError")
                pass

            context = {
                "function_name": "local_lambda",
                "aws_request_id": "local_request_id",
                "invoked_function_arn": "local_function_arn",
                "local": True
            }

            response = lambda_function(event, context)

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'application/json')
            response_bytes = json.dumps(response).encode('utf-8')
            self.send_header('Content-Length', len(response_bytes))
            self.end_headers()
            self.wfile.write(response_bytes)

    PORT = 8000

    with socketserver.TCPServer(("", PORT), LocalLambdaHandler) as httpd:
        print(f"Listening on {get_local_ip()}:{PORT}")
        httpd.serve_forever()

def get_local_ip():
    # Create a socket and connect to an external server to retrieve the local IP address
    # This method is used to determine the local IP address currently in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))  # Connect to a remote server
        local_ip = sock.getsockname()[0]  # Get the local IP address
    finally:
        sock.close()
    return local_ip
	
lambda_runner(lambda_handler)
