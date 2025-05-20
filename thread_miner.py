import hashlib
import time
import threading

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        value = str(self.index) + self.previous_hash + str(self.timestamp) + self.data + str(self.nonce)
        
        return hashlib.sha256(value.encode()).hexdigest()
    
    def mine_block(self, difficulty, stop_event):
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            if stop_event.is_set():
                return
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            stop_event.set()
            print(f"Bloco Minerado com nonce {self.nonce}: {self.hash}")
            
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty 
    
    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty, threading.Event())
        self.chain.append(new_block)
            
def concurrent_mining(num_threads, difficulty):
    latest_block = Block(1, "0", time.time(), "Bloco concorrente")
    stop_event = threading.Event()
    
    def mine():
        block_copy = Block(latest_block.index, latest_block.previous_hash, latest_block.timestamp, latest_block.data)
        block_copy.mine_block(difficulty, stop_event)
        
    threads = []
    start_time = time.time()
    for _ in range(num_threads):
        t = threading.Thread(target=mine)
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
    
    elapsed_time = time.time() - start_time
    print(f"\n Mineracao com {num_threads} threads concluidas em {elapsed_time:.2f} segundos.")
    
if __name__ == "__main__":
    concurrent_mining(num_threads=4,difficulty=4)
        