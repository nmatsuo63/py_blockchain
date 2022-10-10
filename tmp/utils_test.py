import collections
import hashlib

block = {'b': 2, 'a': 1}
block2 = {'a': 1, 'b': 2}

print(hashlib.sha256(str(block).encode()).hexdigest())
print(hashlib.sha256(str(block2).encode()).hexdigest())

def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d:d[0]))

# key=lambda d:d[0]→d[0]=aやbなど辞書のkeyでソートするように指定
# lambdaは無名関数。引数dを受け取ってd[0]を返す
# 参考：https://qiita.com/n10432/items/e0315979286ea9121d57
block = collections.OrderedDict(sorted(block.items(), key=lambda d:d[0]))
block2 = collections.OrderedDict(sorted(block2.items(), key=lambda d:d[0]))

print(hashlib.sha256(str(block).encode()).hexdigest())
print(hashlib.sha256(str(block2).encode()).hexdigest())


print(hashlib.sha256('test2'.encode()).hexdigest())
print(hashlib.sha256('test2'.encode()).hexdigest())
