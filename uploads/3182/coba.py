import docker

client = docker.APIClient(base_url='tcp://127.0.0.1:2375')
# a = client.images.build(path="./")
response = [line for line in client.build(path = "./", rm = True, tag = 'yourname/volume')]
print(response)


