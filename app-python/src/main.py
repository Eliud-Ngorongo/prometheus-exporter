import os
import time
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

from prometheus_client import Gauge, CollectorRegistry, generate_latest

DOCKER_HUB_ORG = os.getenv('DOCKERHUB_ORGANIZATION', 'camunda')
DOCKER_HUB_URL = f'https://hub.docker.com/v2/repositories/{DOCKER_HUB_ORG}/'
UPDATE_INTERVAL = 300  # Update every 5 minutes (300 seconds)
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

custom_registry = CollectorRegistry()

image_pulls_metric = Gauge('docker_image_pulls', 'The total number of Docker image pulls', ['image', 'organization'])

def check_docker_hub_org():
    """
    Check if the DockerHub organization exists.
    """
    try:
        response = requests.get(f"{DOCKER_HUB_URL}?page_size=1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                logging.info("DockerHub organization '%s' exists.", DOCKER_HUB_ORG)
                return True
        elif response.status_code == 404:
            logging.error("DockerHub organization '%s' not found.", DOCKER_HUB_ORG)
            return False
        else:
            logging.error("HTTP error while accessing DockerHub: %s", response.status_code)
            return False
    except requests.exceptions.RequestException as exc:
        logging.error("Error accessing DockerHub: %s", exc)
        return False

def get_image_pulls(cache=None):
    """
    Fetch the number of image pulls for each repository in the DockerHub organization.
    """
    if cache is None:
        cache = {}
    page = 1
    page_size = 25
    retries = 0
    while True:
        url = f"{DOCKER_HUB_URL}?page={page}&page_size={page_size}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data['results']:
                break

            for repo in data['results']:
                image_name = repo['name']
                pulls = repo['pull_count']
                if image_name not in cache or cache[image_name] != pulls:
                    image_pulls_metric.labels(image=image_name, organization=DOCKER_HUB_ORG).set(pulls)
                    cache[image_name] = pulls
        except requests.exceptions.RequestException as exc:
            logging.error("Error fetching data from DockerHub: %s", exc)
            retries += 1
            if retries >= MAX_RETRIES:
                logging.error("Max retries reached. Stopping further attempts.")
                break
            time.sleep(5)
        except Exception as exc:
            logging.exception("Unexpected error occurred: %s", exc)
            break

def update_metrics():
    """
    Periodically update the metrics by fetching the latest data.
    """
    cache = {}
    while True:
        get_image_pulls(cache)
        time.sleep(UPDATE_INTERVAL)

class MetricsHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for serving Prometheus metrics.
    """
    def do_GET(self):
        if self.path == '/metrics':
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
                self.end_headers()
                self.wfile.write(generate_latest(custom_registry))
            except Exception as exc:
                logging.exception("Error generating metrics: %s", exc)
                self.send_error(500, 'Error generating metrics')
        else:
            self.send_response(404)
            self.end_headers()

def run_http_server():
    """
    Start the HTTP server to serve metrics.
    """
    server = HTTPServer(('0.0.0.0', 2113), MetricsHandler)
    server.serve_forever()

def main():
    """
    Main function to start the Prometheus exporter.
    """
    # Check if DockerHub organization exists before starting
    if not check_docker_hub_org():
        logging.error("DockerHub organization '%s' does not exist. Continuing with no data.", DOCKER_HUB_ORG)
     # Start up the custom registry with the metric
    custom_registry.register(image_pulls_metric)
    # Start updating metrics in a separate thread.
    update_metrics_thread = threading.Thread(target=update_metrics)
    update_metrics_thread.start()

    logging.info("Prometheus Exporter started on port 2113")
    run_http_server()

if __name__ == '__main__':
    main()
