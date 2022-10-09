import base58
import codecs
import hashlib
import binascii

from ecdsa import NIST256p
from ecdsa import SigningKey

class Wallet(object):
    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        # 1. Creating a public key with ECDSA
        self._publick_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._publick_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    def generate_blockchain_address(self):
        # 2. SHA-256 for the public key
        public_key_bytes = self._publick_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)#bite public key
        sha256_bpk_digest = sha256_bpk.digest()

        # 3. Ripemd160 for the SHA-256
        ripemd160_bpk = hashlib.new('ripemd160')
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, 'hex')

        # 4. Add network byte
        networ_byte = b'00'#メインネットの場合は00とする
        network_bitcoin_public_key = networ_byte + ripemd160_bpk_hex
        network_bitcoin_public_key_bytes = codecs.decode(network_bitcoin_public_key, ('hex'))

        # 5. Double SHA-256
        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        # 6. Get checksum
        checksum = sha256_hex[:8]

        # 7. Concatenate public key and checksum
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')

        # 8. Encoding the key with Base58
        blockchain_address = base58.b58encode(binascii.unhexlify(address_hex)).decode('utf-8')
        return blockchain_address

if __name__ == '__main__':
    wallet = Wallet()
    print(wallet.private_key)
    print(wallet.public_key)
    print(wallet.blockchain_address)





