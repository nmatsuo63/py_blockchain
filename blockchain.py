# Python標準ライブラリ
import hashlib
import json
import enum
import logging
import sys
import time

# 外部ライブラリ
from ecdsa import NIST256p
from ecdsa import VerifyingKey

# 自作ライブラリ
import utils

MINING_DIFFICULTY = 3  # 何桁目までをゼロにするか
MINING_SENDER = "THE BLOCKCHAIN"  # マイニング報酬の贈り元アドレス
MINING_REWART = 1.0  # マイニング報酬

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class BlockChain(object):
    def __init__(self, blockchain_address=None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address

    def create_block(self, nonce, previous_hash):
        # 引数をまとめてブロックを作成
        block = utils.sorted_dict_by_key(
            {
                "timestamp": time.time(),
                "transactions": self.transaction_pool,
                "nonce": nonce,
                "previous_hash": previous_hash,
            }
        )
        # ブロックをチェーンに追加
        self.chain.append(block)
        # トランザクションプールを初期化
        self.transaction_pool = []
        return block

    def hash(self, block):
        # ブロックからハッシュ値を生成
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(
        self,
        sender_blockchain_address,
        recipient_blockchain_address,
        value,
        sender_public_key=None,
        signature=None,
    ):
        # 引数をまとめてトランザクションを作成
        transaction = utils.sorted_dict_by_key(
            {
                "sender_blockchain_address": sender_blockchain_address,
                "recipient_blockchain_address": recipient_blockchain_address,
                "value": float(value),
            }
        )

        # 送信元がブロックチェーンの場合はトランザクションプールに格納
        if sender_blockchain_address == MINING_SENDER:
            self.transaction_pool.append(transaction)
            return True

        # トランザクション署名が検証できた場合はトランザクションプールに格納
        if self.verify_transaction_signature(sender_public_key, signature, transaction):

            # # 送信者のアドレスに十分なBTCがない場合はエラー
            # if self.calculate_total_amount(sender_blockchain_address) < float(value):
            #     logger.error({'action': 'add_transaction', 'error': 'no_value'})
            #     return False

            self.transaction_pool.append(transaction)
            return True
        return False

    def verify_transaction_signature(self, sender_public_key, signature, transaction):
        # トランザクションをダイジェスト
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode("utf-8"))
        message = sha256.digest()
        # 署名を16進数からバイト形式に変換
        signature_bytes = bytes().fromhex(signature)
        # 送信者の公開鍵を使って検証する
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(sender_public_key), curve=NIST256p
        )
        verified_key = verifying_key.verify(signature_bytes, message)
        return verified_key

    def valid_proof(
        self, transactions, previous_hash, nonce, difficulty=MINING_DIFFICULTY
    ):
        # ブロックを生成してハッシュ値を作成
        guess_block = utils.sorted_dict_by_key(
            {
                "transactions": transactions,
                "nonce": nonce,
                "previous_hash": previous_hash,
            }
        )
        guess_hash = self.hash(guess_block)
        # ハッシュ値の冒頭の0がdifficulty個連続しているか確認
        is_proved = guess_hash[:difficulty] == "0" * difficulty
        if is_proved:
            print("proved_hash:", guess_hash)
        return is_proved

    def proof_of_work(self):
        # トランザクションと前ブロックのハッシュ値を取得
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        is_proved = False
        # プルーフが成功するまでの回数をナンスとする
        while is_proved is False:
            is_proved = self.valid_proof(transactions, previous_hash, nonce)
            nonce += 1
        return nonce

    def mining(self):
        # トランザクションの生成
        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=self.blockchain_address,
            value=MINING_REWART,
        )
        # ナンスの生成（Proof of Workの結果）
        nonce = self.proof_of_work()
        # 前ブロックのハッシュ値を取得
        previous_hash = self.hash(self.chain[-1])
        # ブロックを生成
        self.create_block(nonce, previous_hash)
        # マイニングの結果をログ出力
        logger.info({"action": "mining", "status": "success"})
        return True

    def calculate_total_amount(self, blockchain_address):
        # あるアドレスのBTC総量を計算
        total_amount = 0.0
        for block in self.chain:
            for transaction in block["transactions"]:
                value = float(transaction["value"])
                if blockchain_address == transaction["recipient_blockchain_address"]:
                    total_amount += value
                if blockchain_address == transaction["sender_blockchain_address"]:
                    total_amount -= value
        return total_amount


# if __name__ == "__main__":
#     my_blockchain_address = "__my_blockchain_address__"  # マイナーのアドレス
#     block_chain = BlockChain(blockchain_address=my_blockchain_address)
#     utils.pprint(block_chain.chain)

#     block_chain.add_transaction("A", "B", 1.0)  # AさんからBさんへ1.0BTC送る
#     block_chain.mining()
#     utils.pprint(block_chain.chain)

#     block_chain.add_transaction("C", "D", 2.0)
#     block_chain.add_transaction("X", "Y", 3.0)
#     block_chain.mining()
#     utils.pprint(block_chain.chain)

#     print("my", block_chain.calculate_total_amount(my_blockchain_address))
#     print("C", block_chain.calculate_total_amount("C"))
#     print("D", block_chain.calculate_total_amount("D"))
