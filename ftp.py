#!/bin/env python3

import os
import argparse
import shutil
import sys

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ftp_stop', action='store_true', default=False, help='stop ftp server')
    return parser.parse_args()

def ftp_configure(args):
    ftp_def_loc = "/etc/ftp/defconfig"
    ftp_conf_loc = "/root/FTP"

    ftp_files_map = {
        "/etc/vsftpd.conf": "{}/vsftpd.conf"
    }

    # process default config files
    for org_path, dest_path_pattern in ftp_files_map.items():
        dest_path = dest_path_pattern.format(ftp_def_loc)
        if os.path.exists(os.path.dirname(dest_path)) is False:
            os.makedirs(os.path.dirname(dest_path))

        if os.path.exists(org_path) is True:
            #print("Move: {} -> {}".format(org_path, dest_path_pattern.format(ftp_def_loc)))
            shutil.move(org_path, dest_path_pattern.format(ftp_def_loc))

        #print("Link: {} -> {}".format(org_path, dest_path))
        os.symlink(dest_path, org_path)

    # process specify website type
    for org_path, dest_path_pattern in ftp_files_map.items():
        dest_path = dest_path_pattern.format(ftp_conf_loc)
        os.system("chown -R root:root {}".format(dest_path))

        if os.path.exists(dest_path):
            os.remove(org_path)
            #print("LinkAgain: {} -> {}".format(org_path, dest_path))
            os.symlink(dest_path, org_path)

    # other specify actions
    os.system("adduser test_user1 --gecos '' --disabled-password")
    os.system("echo test_user1:test_user1 | chpasswd")
    os.system("cp -rf {}/ftp_site/* /home/test_user1/".format(ftp_conf_loc))
    os.system("chown -R  test_user1:test_user1 /home/test_user1")
    os.system("chmod -w /home/test_user1")

    print("Start FTP Server => ftp://localhost, user:test_user1, password: test_user1")

    os.system("/etc/init.d/vsftpd restart")

    return 0

def ftp_stop(args):
    os.system("/etc/init.d/vsftpd stop")
    return 0


def main():
    args = process_command()
    if args.ftp_stop:
        return ftp_stop(args)
    else:
        return ftp_configure(args)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        sys.exit(1)

