import rpyc
import yaml
from rpyc.utils.server import ThreadedServer
import threading


@rpyc.service
class LockManager(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.rlock_hash = {}
        self.lock_hash = None

    @rpyc.exposed
    def acquire_lock(self, query):
        if 'select' in query:
            if self.rlock_hash.get(query, -1) == -1:
                self.rlock_hash[query] = 1
            else:
                self.rlock_hash[query] += 1
            print("Rlock: ", self.rlock_hash)
            return True
        else:
            if self.lock_hash is None:
                self.lock_hash = 1
                print("Lock: ", self.lock_hash)
                return True
            else:
                print("Lock: ", self.lock_hash)
                return False

    @rpyc.exposed
    def release_lock(self, query):
        if 'select' in query:
            self.rlock_hash[query] -= 1
        else:
            self.lock_hash = None
        print("Rlock release: ", self.rlock_hash)
        print("Lock release: ", self.lock_hash)


if __name__ == '__main__':
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    port = config['lock_manager']['port']
    host = config['lock_manager']['host']
    print('Lock Manager Started ...')
    server = ThreadedServer(LockManager, port=port, hostname=host)
    server.start()
