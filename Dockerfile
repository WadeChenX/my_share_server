# Create v0.0.1
# Only install package
FROM ubuntu:18.04 
RUN apt-get update 
RUN apt-get --yes -f install apt-utils
RUN apt-get --yes -f install python3 
RUN apt-get --yes -f install vim
RUN apt-get --yes -f install apache2 
RUN apt-get --yes -f install apache2-utils 
RUN apt-get --yes -f install openssl
RUN apt-get --yes -f install vsftpd
RUN apt-get --yes -f install libpam-pwdfile
RUN apt-get --yes -f purge   rpcbind
RUN apt-get --yes -f install nfs-kernel-server
RUN apt-get --yes -f install nfs-common
RUN apt-get --yes -f install samba
RUN apt-get --yes -f install smbclient
RUN apt-get clean 
CMD ["bash"]

