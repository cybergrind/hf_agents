import argparse
import logging
from gradio_client import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger(__name__)

API_NAME = '/get_beam_search_html'
CLIENT_NAME = 'agents-course/decoding_visualizer'


def get_args():
    parser = argparse.ArgumentParser(description='Query the HF Agents API')
    parser.add_argument('--query', default='Name of the current president of USA is')
    return parser.parse_args()


def main():
    args = get_args()
    client = Client(CLIENT_NAME)
    response = client.predict(input_text=args.query, api_name=API_NAME)
    log.info(response)

if __name__ == '__main__':
    main()
