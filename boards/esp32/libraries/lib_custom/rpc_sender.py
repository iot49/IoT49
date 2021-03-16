try:
    import urequests as requests
except:
    import requests 

"""
RPC calls to python objects on host via HTTP Post
"""

class RPC_Exception(Exception):
    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code
        self.msg = msg

class _Dispatcher:
    def __init__(self, receiver_address, resource_name, resource_id):
        self.receiver_address = receiver_address
        self._resource_name = resource_name
        self._resource_id = resource_id

    def __getattr__(self, name):
        def method(*args, **kwargs):
            # print("call {}({}, {}) on {}".format(name, args, kwargs, self._resource_id))
            res = requests.post("{}/call_method".format(self.receiver_address), json={
                'resource_id': self._resource_id,
                'method': name,
                'args': args, 'kwargs': kwargs })
            if res.status_code != 200:
                raise RPC_Exception(res.status_code, res.json())
            return res.json()
        return method

    def __str__(self):
        return "Remote object {}".format(self._resource_name)

    def release_resource(self):
        if self._resource_id:
            res = requests.post("{}/release_resource".format(self.receiver_address),
                json={ 'resource_id': self._resource_id })
            if res.status_code != 200:
                raise RPC_Exception(res.status_code, res.json())
            self._resource_name = self._resource_name + " (released)"
            self._resource_id = None
        return self

# connect to a resource on the receiver (host)
# see rpc_receiver for available resources
# arguments:
#    receiver_address, e.g. "http://mac15.home:8080"
#    resource_name, one of TestObj, pwr, scope, dmm
#       (see rpc_receiver for up-to-date list)
# return:
#    handle to remote object, behaves as if it was local, e.g.
#    e.g. handle.foo(1, 2, [3, 4])
def get_resource(receiver_address, resource_name):
    res = requests.post("{}/get_resource".format(receiver_address),
        json={ 'resource': resource_name })
    if res.status_code != 200:
        raise RPC_Exception(res.status_code, res.json())
    return _Dispatcher(receiver_address, resource_name, res.json())
