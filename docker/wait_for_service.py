import argparse
import os
import socket
import time


def wait_for_socket(address, count=20):
    with socket.socket() as s:
        for i in range(count):
            print('Wait for {}:{}, seconds left: {}'.format(*address, count - 1))
            try:
                s.connect(address)
                break
            except socket.error:
                time.sleep(1)


def wait_for_db():
    wait_for_socket((os.environ.get('DB_HOST'), int(os.environ.get('DB_PORT'))))


def wait_for_redis():
    wait_for_socket((os.environ.get('REDIS_HOST'), int(os.environ.get('REDIS_PORT'))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('service', type=str, choices=('db', 'redis'))
    args = parser.parse_args()

    if args.service is None:
        raise argparse.ArgumentError('`SERVICE` argument must be not empty.')

    services = {
        'db': wait_for_db,
        'redis': wait_for_redis,
    }

    services.get(parser.parse_args().service)()
