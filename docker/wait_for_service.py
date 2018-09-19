import argparse
import os
import socket
import time


def wait_for_socket(address, count=20):
    with socket.socket() as s:
        for i in range(count):
            print('Wait for {}:{}, seconds left: {}'.format(*address, count - i))
            try:
                s.connect(address)
                break
            except socket.error:
                time.sleep(1)
        else:
            print('Service {}:{} unavailable.'.format(*address))
            raise SystemExit(1)


def wait_for_db():
    wait_for_socket((os.environ.get('DB_HOST'), int(os.environ.get('DB_PORT'))))


def wait_for_redis():
    wait_for_socket((os.environ.get('REDIS_HOST'), int(os.environ.get('REDIS_PORT'))))


def wait_for_server():
    wait_for_socket((os.environ.get('SERVER_HOST'), int(os.environ.get('SERVER_PORT'))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('service', type=str, choices=('db', 'redis', 'server'))
    args = parser.parse_args()

    if args.service is None:
        raise argparse.ArgumentError('`SERVICE` argument must be not empty.')

    services = {
        'db': wait_for_db,
        'redis': wait_for_redis,
        'server': wait_for_server
    }

    services.get(parser.parse_args().service)()
