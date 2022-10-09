import collections

# key=lambda d:d[0]→d[0]=aやbなど辞書のkeyでソートするように指定
# lambdaは無名関数。引数dを受け取ってd[0]を返す
# 参考：https://qiita.com/n10432/items/e0315979286ea9121d57
def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d:d[0]))


