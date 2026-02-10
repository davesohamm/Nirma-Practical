from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Automatically discover running backend servers
def discover_servers(base="http://localhost", start_port=5001, end_port=5010):
    servers = []
    print("[DISCOVERY] Scanning for backend servers...")
    for port in range(start_port, end_port + 1):
        url = f"{base}:{port}/accounts"
        try:
            resp = requests.get(url, timeout=1)
            if resp.status_code < 500:  # reachable
                servers.append(f"{base}:{port}")
                print(f"[DISCOVERY] ✅ Found backend: {base}:{port}")
        except requests.exceptions.RequestException:
            pass
    if not servers:
        print("[DISCOVERY] ❌ No servers found in range!")
    return servers


# Discover backends automatically at startup
backend_servers = discover_servers()
current_index = 0


def get_next_server():
    global current_index
    if not backend_servers:
        return None
    server = backend_servers[current_index]
    current_index = (current_index + 1) % len(backend_servers)
    return server


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def load_balancer(path):
    backend_server = get_next_server()
    if not backend_server:
        return Response("No backend servers available.\n", status=502)

    print(f"[LOAD BALANCER] Forwarding '{request.method} {path}' → {backend_server}")

    try:
        resp = requests.request(
            method=request.method,
            url=f"{backend_server}/{path}",
            headers={k: v for k, v in request.headers if k != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        print(f"[LOAD BALANCER] Response from {backend_server} → Status {resp.status_code}")

        response = Response(resp.content, resp.status_code, dict(resp.headers))
        response.headers["Response-From"] = backend_server
        return response

    except Exception as e:
        print(f"[LOAD BALANCER] Error contacting {backend_server}: {e}")
        return Response("Backend server error.\n", status=502)


if __name__ == "__main__":
    print("[LOAD BALANCER] Starting on port 5004...")
    print("[LOAD BALANCER] Discovering backends dynamically...")
    app.run(port=5004)
