#!/bin/env python3

import os
import argparse
import shutil
import sys

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--samba_stop', action='store_true', default=False, help='stop samba server')
    return parser.parse_args()

def samba_configure(args):
    samba_def_loc = "/etc/samba/defconfig"
    samba_conf_loc = "/root/SAMBA"

    samba_files_map = {
            "/etc/samba/smb.conf": "{}/smb.conf"
    }

    # process default config files
    for org_path, dest_path_pattern in samba_files_map.items():
        dest_path = dest_path_pattern.format(samba_def_loc)
        if os.path.exists(os.path.dirname(dest_path)) is False:
            os.makedirs(os.path.dirname(dest_path))

        if os.path.exists(org_path) is True:
            #print("Move: {} -> {}".format(org_path, dest_path_pattern.format(samba_def_loc)))
            shutil.move(org_path, dest_path_pattern.format(samba_def_loc))

        #print("Link: {} -> {}".format(org_path, dest_path))
        os.symlink(dest_path, org_path)

    # process specify website type
    for org_path, dest_path_pattern in samba_files_map.items():
        dest_path = dest_path_pattern.format(samba_conf_loc)

        if os.path.exists(dest_path):
            os.remove(org_path)
            #print("LinkAgain: {} -> {}".format(org_path, dest_path))
            os.symlink(dest_path, org_path)

    # other specific
    os.system("adduser smbuser --gecos '' --disabled-password")
    os.system("echo smbuser:smbuser | chpasswd")
    os.system("(echo smbuser; echo smbuser) | smbpasswd -s -a smbuser")
    os.system("mount --bind /root/SAMBA/site /home/smbuser")

    print("Start SAMBA Server => //localhost/public, physical root: /root/SAMBA/site, user:smbuser, password:smbuser")

    os.system("/etc/init.d/smbd restart")

def samba_stop(args):
    os.system("/etc/init.d/smbd stop")
    os.system("umount /home/smbuser")


def main():
    args = process_command()
    if args.samba_stop:
        return samba_stop(args)
    else:
        return samba_configure(args)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        sys.exit(1)

