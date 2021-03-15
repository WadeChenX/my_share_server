#!/bin/env python3

import os
import argparse
import shutil
import sys

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apache_type', type=str, default="HTTP", help='Specify website type')
    parser.add_argument('--apache_stop', action='store_true', default=False, help='stop apache server')
    return parser.parse_args()

def apache_configure(args):
    apache_def_loc = "/etc/apache2/defconfig"
    http_conf_loc = "/root/HTTP"
    https_conf_loc = "/root/HTTPS"
    website_loc = '/var/www/html'

    apache2_files_map = {
            "/var/www/html": "{}/website",
            "/etc/apache2/apache2.conf": "{}/apache2.conf",
            "/etc/apache2/sites-available/default-ssl.conf": "{}/sites-available/default-ssl.conf"
    }

    if args.apache_type.upper() != "HTTP" and args.apache_type.upper() != "HTTPS":
        print("ERROR: invalid parameters. {}".format(args.apache_type))
        return -1

    # process default config files
    for org_path, dest_path_pattern in apache2_files_map.items():
        dest_path = dest_path_pattern.format(apache_def_loc)
        if os.path.exists(os.path.dirname(dest_path)) is False:
            os.makedirs(dest_path)

        if os.path.exists(org_path) is True:
            #print("Move: {} -> {}".format(org_path, dest_path_pattern.format(apache_def_loc)))
            shutil.move(org_path, dest_path_pattern.format(apache_def_loc))

        #print("Link: {} -> {}".format(org_path, dest_path))
        os.symlink(dest_path, org_path)

    print("website type: {}".format(args.apache_type))

    # process specify website type
    for org_path, dest_path_pattern in apache2_files_map.items():
        dest_path = ""
        if args.apache_type.upper() == "HTTP":
            dest_path = dest_path_pattern.format(http_conf_loc)

        elif args.apache_type.upper() == "HTTPS":
            dest_path = dest_path_pattern.format(https_conf_loc)

        if os.path.exists(dest_path):
            os.remove(org_path)
            #print("LinkAgain: {} -> {}".format(org_path, dest_path))
            os.symlink(dest_path, org_path)

    # other specify actions
    if args.apache_type.upper() == "HTTPS":
        os.system("a2enmod ssl")
        os.system("a2ensite default-ssl.conf")

    print("Start Aapache Server => {}://localhost".format(args.apache_type.lower()))

    os.system("/etc/init.d/apache2 restart")

def apache_stop(args):
    os.system("/etc/init.d/apache2 stop")


def main():
    args = process_command()
    if args.apache_stop:
        return apache_stop(args)
    else:
        return apache_configure(args)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        sys.exit(1)

