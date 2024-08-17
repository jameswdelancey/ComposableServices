import http.server
import socketserver
import json
import importlib.util


# Define the handler for the HTTP server
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Load routes from config file
        with open("routes.json", "r") as f:
            routes = json.load(f)

        # Check if the path exists in routes
        if self.path in routes:
            # Dynamically load the module and call the function
            func_name = routes[self.path]
            try:
                # Assume that the functions are defined in a file called functions.py
                spec = importlib.util.spec_from_file_location(
                    "functions", "functions.py"
                )
                functions = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(functions)

                # Get the function by name
                if hasattr(functions, func_name):
                    func = getattr(functions, func_name)
                    content_type, code, response = func()
                    self.send_response(code or 200)
                    self.send_header("Content-type", content_type or "text/html")
                    self.end_headers()
                    self.wfile.write(response)
                    return
                else:
                    self.send_error(
                        404, f"Function '{func_name}' not found in functions.py"
                    )
            except FileNotFoundError:
                self.send_error(404, "functions.py not found")
        else:
            self.send_error(404, f"Route '{self.path}' not found in routes.json")

        return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Set the port
PORT = 8000

# Create an object of the above class
handler_object = MyHttpRequestHandler

# Create a server
with socketserver.TCPServer(("", PORT), handler_object) as httpd:
    print("Server started at localhost:" + str(PORT))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

print("Server stopped.")
