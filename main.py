import yaml
import os


with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

lock_manager_host = input("Enter the host of the lock manager: ")
coordinator_host = input("Enter the host of the coordinator: ")
app_host = input("Enter the host of the app: ")

config['lock_manager']['host'] = lock_manager_host
config['coordination']['host'] = coordinator_host
config['app']['host'] = app_host
config['socket_ping']['host'] = app_host

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)
    f.close()

# run commands in terminal
for i in [lock_manager_host, coordinator_host, app_host]:
    command = f"scp -i ./distributed.pem config.yaml ec2-user@{i}:/home/ec2-user/"
    os.system(command)
