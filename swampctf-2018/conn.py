import socket

class Conn:
    def __init__(self, host='chal1.swampctf.com', port=1450, verbose=True):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.s.settimeout(5.)
        self.verbose = verbose
    
    def read(self):
        result = self.s.recv(1024).strip()
        if self.verbose:
            print(result.decode('ascii'))       
        return result
    
    def send(self, data, sleep=False):
        self.s.sendall(data + b"\n")
        if sleep:
            time.sleep(sleep)
        result = self.s.recv(1024).strip()
        
        if self.verbose:
            print(data.decode('ascii'), "->", result.decode('ascii'))       
        return result
    
    def close(self):
        self.s.close()
