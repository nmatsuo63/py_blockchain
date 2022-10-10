import base58
import codecs
import hashlib
import binascii
import os, sys

from ecdsa import NIST256p
from ecdsa import SigningKey

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import utils


class Wallet(object):
    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        # 1. Creating a public key with ECDSA
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        # 2. SHA-256 for the public key
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)  # bite public key
        sha256_bpk_digest = sha256_bpk.digest()

        # 3. Ripemd160 for the SHA-256
        ripemed160_bpk = hashlib.new("ripemd160")
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, "hex")

        # 4. Add network byte
        network_byte = b"00"  # メインネットの場合は00とする
        network_bitcoin_public_key = network_byte + ripemed160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, "hex"
        )

        # 5. Double SHA-256
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, "hex")

        # 6. Get checksum
        checksum = sha256_hex[:8]

        # 7. Concatenate public key and checksum
        address_hex = (network_bitcoin_public_key + checksum).decode("utf-8")

        # 8. Encoding the key with Base58
        blockchain_address = base58.b58encode(binascii.unhexlify(address_hex)).decode(
            "utf-8"
        )
        return blockchain_address


class Transaction(object):
    def __init__(
        self,
        sender_private_key,
        sender_public_key,
        sender_blockchain_address,
        recipient_blockchain_address,
        value,
    ):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_blockchain_address = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value

    def generate_signature(self):
        # トランザクションを生成
        sha256 = hashlib.sha256()
        transaction = utils.sorted_dict_by_key(
            {
                "sender_blockchain_address": self.sender_blockchain_address,
                "recipient_blockchain_address": self.recipient_blockchain_address,
                "value": float(self.value),
            }
        )
        # トランザクションをUTF-8に変換
        sha256.update(str(transaction).encode("utf-8"))
        # メッセージを生成
        message = sha256.digest()
        # 公開鍵に適合する秘密鍵を取り出す
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p
        )
        # 秘密鍵に署名する
        private_key_sign = private_key.sign(message)
        # 署名を16進数に変換
        signature = private_key_sign.hex()
        return signature


if __name__ == "__main__":
    wallet_Miner = Wallet()
    wallet_A = Wallet()
    wallet_B = Wallet()

    t = Transaction(
        wallet_A.private_key,
        wallet_A.public_key,
        wallet_A.blockchain_address,
        wallet_B.blockchain_address,
        1.0,
    )

    ############ Blockchain Node #############
    import blockchain

    block_chain = blockchain.BlockChain(
        blockchain_address=wallet_Miner.blockchain_address
    )
    is_added = block_chain.add_transaction(
        wallet_A.blockchain_address,
        wallet_B.blockchain_address,
        1.0,
        wallet_A.public_key,
        t.generate_signature(),
    )
    print("Added?", is_added)
    block_chain.mining()
    utils.pprint(block_chain.chain)

    print("A", block_chain.calculate_total_amount(wallet_A.blockchain_address))
    print("B", block_chain.calculate_total_amount(wallet_B.blockchain_address))
