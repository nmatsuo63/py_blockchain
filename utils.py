import collections
import logging
import re
import socket

logger = logging.getLogger(__name__)

# 192.168.0.24とすると、(?P<prefix_host>^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.)が192.168.0に相当
# d{1,3}は1-3桁分という意味
RE_IP = re.compile('(?P<prefix_host>^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.)(?P<last_ip>\\d{1,3}$)')

# key=lambda d:d[0]→d[0]=aやbなど辞書のkeyでソートするように指定
# lambdaは無名関数。引数dを受け取ってd[0]を返す
# 参考：https://qiita.com/n10432/items/e0315979286ea9121d57
def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(sorted(unsorted_dict.items(), key=lambda d: d[0]))


def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            if k == "transactions":
                print(k)
                for d in v:
                    print(f"-" * 40)
                    for kk, vv in d.items():
                        print(f"{kk:30}{vv}")
            else:
                print(f"{k:15}{v}")
    print(f'{"-"*59}')

def is_found_host(target, port):
    # target: IPアドレス
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            # targetとportをタプルで渡す
            sock.connect((target, port))
            return True
        except Exception as ex:
            logger.error({
                'action': 'is_found_host',
                'target': target,
                'port': port,
                'ex': ex
            })
            return False

def find_neighbours(my_host, my_port, start_ip_range, end_ip_range, start_port, end_port):
    # 192.168.0.24 (1, 3)
    address = f'{my_host}:{my_port}'
    m = RE_IP.search(my_host)
    if not m:
        return None
    prefix_host = m.group('prefix_host')
    last_ip = m.group('last_ip')

    neighbours = []
    for guess_port in range(start_port, end_port):
        for ip_range in range(start_ip_range, end_ip_range):
            guess_host = f'{prefix_host}{int(last_ip)+int(ip_range)}'
            guess_address = f'{guess_host}:{guess_port}'
            if is_found_host(guess_host, guess_port) and not guess_address == address:
                neighbours.append(guess_address)
    return neighbours


if __name__ == '__main__':
    print(is_found_host('127.0.0.1', 5100))
    # 192.168.0.24 - 192.168.0.22 - 30

    print(find_neighbours('192.168.1.3', 5100, 0, 3, 5100, 5103))





