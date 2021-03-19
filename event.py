#!/bin/env python3

import os
import argparse
import shutil
import sys
import subprocess
import signal

SERVER_NAME = 'event_app'
SERVER_FILE = './{}.py'.format(SERVER_NAME)
SERVER_PID_PATH='/tmp/{}.pid'.format(SERVER_NAME)
SERVER_PORT = 5000

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--event_stop', action='store_true', default=False, help='stop Event server')
    return parser.parse_args()

def event_configure(args):
    args = '--server_port={}'.format(SERVER_PORT)

    print("Start Event Server => http://localhost:{}".format(SERVER_PORT))
    os.system('python3 {} {} & echo $! > {}'.format(SERVER_FILE, args, SERVER_PID_PATH))


def event_stop(args):
    with open('{}'.format(SERVER_PID_PATH), 'r') as f:
        server_pid = int(f.read())

    os.kill(server_pid, signal.SIGINT)
    os.remove(SERVER_PID_PATH)

def main():
    args = process_command()
    if args.event_stop:
        return event_stop(args)
    else:
        return event_configure(args)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        sys.exit(1)

