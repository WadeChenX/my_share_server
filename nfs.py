#!/bin/env python3

import os
import argparse
import shutil
import sys

def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nfs_stop', action='store_true', default=False, help='stop NFS server')
    return parser.parse_args()

def nfs_configure(args):
    nfs_def_loc = "/etc/nfs/defconfig"
    nfs_conf_loc = "/root/NFS"

    nfs_files_map = {
            "/etc/exports": "{}/exports"
    }

    # process default config files
    for org_path, dest_path_pattern in nfs_files_map.items():
        dest_path = dest_path_pattern.format(nfs_def_loc)
        if os.path.exists(os.path.dirname(dest_path)) is False:
            os.makedirs(os.path.dirname(dest_path))

        if os.path.exists(org_path) is True:
            #print("Move: {} -> {}".format(org_path, dest_path_pattern.format(nfs_def_loc)))
            shutil.move(org_path, dest_path_pattern.format(nfs_def_loc))

        #print("Link: {} -> {}".format(org_path, dest_path))
        os.symlink(dest_path, org_path)

    # process specify website type
    for org_path, dest_path_pattern in nfs_files_map.items():
        dest_path = dest_path_pattern.format(nfs_conf_loc)

        if os.path.exists(dest_path):
            os.remove(org_path)
            #print("LinkAgain: {} -> {}".format(org_path, dest_path))
            os.symlink(dest_path, org_path)

    print("Start NFS Server => nfs://localhost, physical root: /root/NFS/site, virtual root: /")

    os.system("/etc/init.d/rpcbind restart")
    os.system("/etc/init.d/nfs-kernel-server restart")

def nfs_stop(args):
    os.system("/etc/init.d/nfs-kernel-server stop")


def main():
    args = process_command()
    if args.nfs_stop:
        return nfs_stop(args)
    else:
        return nfs_configure(args)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        print(e)
        sys.exit(1)

