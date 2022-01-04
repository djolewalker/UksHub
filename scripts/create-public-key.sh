cd ..
rm /root/.ssh/id_rsa.pub
rm /root/.ssh/id_rsa
ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa