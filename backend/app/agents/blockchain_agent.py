import hashlib
import json
import time


class BlockchainAgent:

    def create_block(self, data):

        block = {
            "data": data,
            "timestamp": time.time()
        }

        block_string = json.dumps(block, sort_keys=True).encode()

        block_hash = hashlib.sha256(block_string).hexdigest()

        return {
            "block_hash": block_hash,
            "status": "Recorded on blockchain",
            "timestamp": block["timestamp"]
        }