import http.server
import socketserver
import json
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from lambda_function import lambda_handler

def lambda_runner(lambda_function):
    class LocalLambdaHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/favicon.ico':
                self.send_response(HTTPStatus.OK)
                return

            parsed_url = urlparse(self.path)
            query_params = {key: value[0] for key, value in parse_qs(parsed_url.query).items()}

            event = {
                "httpMethod": "GET",
                "queryStringParameters": query_params,
                "path": parsed_url.path,
                "headers": dict(self.headers),
            }

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
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

lambda_runner(lambda_handler)
