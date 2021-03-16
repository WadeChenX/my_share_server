#!/bin/bash
declare -A support_cmd_map
declare -A cmd_arg_map
declare -A cmd_stop_arg_map

support_cmd_map=( \
    ["apache"]="/root/apache.py"  \
    ["ftp"]="/root/ftp.py"  \
    ["nfs"]="/root/nfs.py"  \
    ["samba"]="/root/samba.py"  \
    ["metric"]="/root/metric.py"  \
    ["bash"]=""  \
)
cmd_arg_map=( \
    ["apache"]="" \
    ["ftp"]="" \
    ["nfs"]="" \
    ["samba"]="" \
    ["metric"]="" \
    ["bash"]="" \
)

cmd_stop_arg_map=( \
    ["apache"]="--apache_stop" \
    ["ftp"]="--ftp_stop" \
    ["nfs"]="--nfs_stop" \
    ["samba"]="--samba_stop" \
    ["metric"]="--metric_stop" \
    ["bash"]="" \
)

SRVS="Unknown"

trap ctrl_c INT

exit_flag=""

function ctrl_c() 
{
    echo "** Trapped CTRL-C. Close services ..."
    exit_flag="1"

    if [ "$SRVS" = "bash" ]; then
        exit
    else
        for entry in $SRVS; do
            echo "Stop $entry service ..."
            cmd=${support_cmd_map[$entry]} 
            arg=${cmd_stop_arg_map[$entry]}
            echo "cmd: $cmd $arg"
            python3 $cmd $arg
        done
    fi
}

function parseParameters() 
{
    old_ifs=$IFS
    IFS=,
    SRVS=
    for entry in $1; do
        if [ -n "${support_cmd_map["$entry"]}" ]; then
            SRVS="$SRVS $entry"
        else
            echo "Unknown service: $entry"
            return 1
        fi
    done
    IFS=$old_ifs

    #for cmd in "${!support_cmd_map[@]}"; do
    #    if [ "$1" = "$cmd" ]; then
    #        SRV=$1
    #        break
    #    fi
    #done
    if [ -z "$SRVS" ]; then
        echo "No service !!"
        return 1
    fi
    shift


    while [ $# -ne 0 ]
    do
        for cmd in "${!support_cmd_map[@]}"; do
            is_arg_belong2cmd=$(echo $1 | grep ^--$cmd)
            if [ "$is_arg_belong2cmd" != "" ]; then
                cmd_arg_map["$cmd"]=${cmd_arg_map["$cmd"]}" $1"
                break
            fi
        done
        if [ "$is_arg_belong2cmd" = ""  ]; then
            echo "Unknwon argument !! " $1
            return 1
        fi
        shift
    done

    #echo "============ DEBUG ============="
    #for cmd in "${!support_cmd_map[@]}"; do
    #    echo $cmd: ${cmd_arg_map["$cmd"]}
    #done
    #echo "============ DEBUG ============="
}

# let apache could browse this directory
chmod 715 /root

if ! parseParameters $@; then
    echo "Error in parseParameters"
    exit 1
fi

if [ "$SRVS" = "bash" ]; then
    bash
else
    for srv in $SRVS; do
        echo "Start $srv website ..."
        # all service MUST start in background
        python3 ${support_cmd_map["$srv"]} ${cmd_arg_map["$srv"]}
        echo "OK"
    done
    echo "Press Ctrl+C to exit ..."
    while [ "$exit_flag" = "" ]; do
        echo "wait" > /dev/null
        sleep 1
    done
fi



#if [ -f "/root/root.sh" ]; then
#    bash -f "/root/root.sh"
#fi
