# Create v0.0.2
# Configure directory structure
FROM my_servers:v0.0.1
# HTTP
EXPOSE 80
# HTTPS
EXPOSE 443
# FTP
EXPOSE 21
# nfs
EXPOSE 111
EXPOSE 2049
# samba
EXPOSE 137
EXPOSE 138
EXPOSE 139
EXPOSE 445
# metric service
EXPOSE 5000
ADD entry.sh /root/
ADD apache.py /root/
ADD ftp.py /root/
ADD nfs.py /root/
ADD samba.py /root/
ADD event.py /root/
ADD event_app.py /root/
ADD bottle.py /root/
WORKDIR /root/
ENTRYPOINT ["/bin/bash", "/root/entry.sh"]
#CMD ["/bin/bash"]

