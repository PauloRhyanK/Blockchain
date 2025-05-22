import hashlib
import time
import threading
import json
import matplotlib.pyplot as plt



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
    
    def mine_block(self, difficulty, stop_event, MinerTimers=False):
        prefix = '0' * difficulty
        timeA = time.time()
        while not self.hash.startswith(prefix):
            # print(f"Tentativa de mineração com nonce {self.nonce}: {self.hash}")
            if stop_event.is_set():
                return False

            # print(f"Tentativa de mineração com nonce {self.nonce}: {self.hash} (Thread: {threading.current_thread().name})")
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        if not stop_event.is_set():
            timeMiner = {"index": self.index, "time": time.time() - timeA}
            print(f"Bloco Minerado com nonce {self.nonce}: {self.hash} (Thread: {threading.current_thread().name}) Tempo: {timeMiner['time']:.2f}s")
            if(MinerTimers != False):
                MinerTimers.append(timeMiner);            
            stop_event.set()
            return True
        else:
            return False
        
        
            
class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty 
    
    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def get_latest_index(self):
        last_block = self.get_latest_block()
        if(last_block):
            return last_block.index;
        return 0
    
    def check_duplicate_hash(self, hash):
        for index_chain in range(len(self.chain)):
            if self.chain[index_chain].hash == hash:
                return False
        return True
    
    def check_block(self, new_block):
        if not self.check_duplicate_hash:
            return False
        if self.get_latest_block().hash != new_block.previous_hash:
            return False
        return True
    
    def check_blockchain(self):
        validChain = True
        previous_block = self.chain[0]
        
        invalid_blocks = []
        for indexBlock in range(1,len(self.chain)):
            current_block = self.chain[indexBlock]
            if previous_block.hash != current_block.previous_hash:
                invalid_blocks.append(current_block.index)
                validChain = False
            previous_block = current_block
            
        if not validChain:
            print(F" \n Blockchain invalido! \n Os seguintes blocos apresentam inconsistencias.")
            for index in range(len(invalid_blocks)):
                print(F"Bloco index: {self.chain[invalid_blocks[index]].index}")
        else:
            print("Blockchain Válido!")
        return validChain
            
            
            
    
    def add_block(self, new_block, stop_event, MinerTimers = False):
        new_block.previous_hash = self.get_latest_block().hash
        if(MinerTimers != False):
            sucessMiner = new_block.mine_block(self.difficulty, stop_event, MinerTimers=MinerTimers)
        else:
            sucessMiner = new_block.mine_block(self.difficulty, stop_event)
        
        if(sucessMiner and self.check_block(new_block)):
            self.chain.append(new_block)
    
    
        
            
def concurrent_mining(num_threads, difficulty = 2, newBlock = False ,blockchain = False, MinerTimers = False):
    
    block_existing = False
    if(newBlock and blockchain):
        block_existing = True; 
        latest_block = newBlock
    else: 
        latest_block = Block(1, "0", time.time(), "Bloco concorrente")
    stop_event = threading.Event()
    
    def mine():
        block_copy = Block(latest_block.index, latest_block.previous_hash, latest_block.timestamp, latest_block.data)
        if(block_existing):
            if(MinerTimers != False):
                blockchain.add_block(block_copy, stop_event, MinerTimers=MinerTimers);
            else:
                blockchain.add_block(block_copy, stop_event);
        else:
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
    # concurrent_mining(num_threads=4,difficulty=2)

    queueDataList = [
        "Alonso passo 20 Blockcoin para ZecaUrubu",
        "Patolino passou 12919 BlockCoin para Pernalonga",
        "Finn passou 69 BlockCoin para FirePrincess",
        "Mickey passou 150 Blockcoin para Minnie",
        "Goku passo 5000 BlockCoin para Vegeta",
        "Batman passou 75 BlockCoin para Robin",
        "Mario passo 100 Blockcoin para Luigi",
        "Tony Stark passo 10000 Blockcoin para Peter Parker",
        "BobEsponja passo 5 Blockcoin para PatrickEstrela",
        "Burro passou 88 BlockCoin para Shrek",
    ]
    # print(json.dumps(testeBlock.get_latest_block().__dict__))
    
    num_threads = [1,2,4,8]
    for number in num_threads:
        bookChain = Blockchain(4)
        bookChain.create_genesis_block()   
        MinerTimers = []
        for i in range(0,len(queueDataList)):
            newBlock = Block(bookChain.get_latest_index() + 1, bookChain.get_latest_block().previous_hash, time.time(), queueDataList[i] )
            concurrent_mining(num_threads=number, newBlock=newBlock, blockchain=bookChain, MinerTimers= MinerTimers)
        bookChain.check_blockchain()
        x = []
        y = []
        for i in range(len(MinerTimers)):
            x.append(MinerTimers[i]["index"])
            y.append(MinerTimers[i]["time"])
        label = str(number) + " threads"
        plt.plot(x, y, marker='o', label=label)
    plt.figlegend(["1 Thread","2 Threads","4 Threads","8 Threads"])
        

    plt.title("Grafico de tempo")
    plt.xlabel("Bloco")
    plt.ylabel("Tempo")
    plt.grid(True,linestyle=':', alpha=0.7)
    plt.savefig("minetimer.png")
    # print(json.dumps([block.__dict__ for block in bookChain.chain], indent=4))
              
       
    
    
   
    
    
    # testeBlock = Blockchain(4)
    # testeBlock.create_genesis_block()       
    # MinerTimers = []
    # for i in range(0,len(queueDataList)):
    #     newBlock = Block(testeBlock.get_latest_index() + 1, testeBlock.get_latest_block().previous_hash, time.time(), queueDataList[i] )
    #     concurrent_mining(num_threads=8, newBlock=newBlock, blockchain=testeBlock, MinerTimers= MinerTimers)
    # x = []
    # y = []
    # for i in range(len(MinerTimers)):
    #     x.append(MinerTimers[i]["index"])
    #     y.append(MinerTimers[i]["time"])
    # 
    
    
    
    
    
    
        