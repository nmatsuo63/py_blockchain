import collections

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
