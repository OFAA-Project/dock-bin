[Enable API port]
- Edit the docker service file
  sudo systemctl edit docker.service
  
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock -H tcp://0.0.0.0:2375

- Save the modified file
- Make sure the Docker service notices the modified configuration

    systemctl daemon-reload

- Restart the Docker service  

    sudo service docker restart
    
- Test
    curl http://localhost:2375/version


running command

sudo python3 dockerbin.py
