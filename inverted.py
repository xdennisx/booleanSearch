import pandas as pd
import jieba
import re
import time

def load_data(file_name):
    df = pd.read_csv(file_name, delimiter = ',',header = None, usecols = [1])
    return df

class TrieNode(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.data = {}
        self.is_word = False
        self.count = 0
        self.invert_index = []

class Trie(object):
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, index):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        # print(word)
        node = self.root
        for letter in word:
            child = node.data.get(letter)
            # print(child)
            if not child:
                node.data[letter] = TrieNode()
            node = node.data[letter]
        node.is_word = True
        if index not in node.invert_index:
            node.count += 1
            node.invert_index.append(index)

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node = self.root
        for letter in word:
            node = node.data.get(letter)
            if not node:
                return False
        # for item in node.invert_index:
        #     print(item)
        # print(node.is_word)
        return node.invert_index  # 判断单词是否是完整的存在在trie树中

if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()
    
    t0 = time.time()
    source = load_data(args.source)
    source_len = len(source)
    trie = Trie()
    r='[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~「」【】／、？：〈〉…（）《》！％－〝〞，＠1-9]+'
    jieba.set_dictionary('dict.txt.big')
    for i in range(0,source_len):
        sentence = source.iat[i,0]
        line=re.sub(r,' ',sentence)
        line_len = len(line)
        # print(line_len)
        # words1 = jieba.lcut(line, cut_all=False)
        # for word in words1:
        #     if len(word) > 1:
        #         trie.insert(word, i+1)
        words2 = jieba.lcut(line, cut_all=True)
        for index, word in enumerate(words2):
            l = len(word)
            words_len = len(words2)
            if l > 1:
                trie.insert(word, i+1)
            if l == 1:
                find_index = line.find(word)
                if find_index == 0:
                    if line_len > 1:
                        trie.insert(word + line[1], i+1)
                    if line_len > 2:
                        trie.insert(word + line[1] + line[2], i+1)
                elif find_index == 1:
                    trie.insert(line[0] + word, i+1)
                    if line_len > 2:
                        trie.insert(word + line[2], i+1)
                        trie.insert(line[0] + word + line[2], i+1)
                    if line_len > 3:
                        trie.insert(word + line[2] + line[3], i+1)
                elif find_index == line_len-1:
                    trie.insert(line[find_index-1] + word, i+1)
                    trie.insert(line[find_index-2] + line[find_index-1] + word, i+1)
                elif find_index == line_len-2:
                    trie.insert(line[find_index-1] + word, i+1)
                    trie.insert(word + line[find_index+1], i+1)
                    trie.insert(line[find_index-2] + line[find_index-1] + word, i+1)
                    trie.insert(line[find_index-1] + word + line[find_index+1], i+1)
                else:
                    trie.insert(line[find_index-2] + line[find_index-1] + word, i+1)
                    trie.insert(line[find_index-1] + word + line[find_index+1], i+1)
                    trie.insert(word + line[find_index+1] + line[find_index+2], i+1)
                    trie.insert(line[find_index-1] + word, i+1)
                    trie.insert(word + line[find_index+1], i+1)
            if l == 2:
                find_index = line.find(word)
                if find_index == 0:
                    if line_len > 2:
                        trie.insert(word + line[2], i+1)
                        trie.insert(word[1] + line[2], i+1)
                elif find_index == line_len-2:
                    trie.insert(line[find_index-1] + word, i+1)
                    trie.insert(line[find_index-1] + word[0], i+1)
                else:
                    trie.insert(line[find_index-1] + word, i+1)
                    trie.insert(line[find_index-1] + word[0], i+1)
                    trie.insert(word + line[find_index+2], i+1)
                    trie.insert(word[1] + line[find_index+2], i+1)

    query = open(args.query, "r", encoding="UTF-8")
    lines = query.readlines()
    file = open(args.output, 'w')
    count = 1
    count_lines = len(lines)
    for x in lines:
        x = x[:len(x)-1]
        print(x)
        op = x.split(' ')
        query_times = (len(op) + 1) / 2
        print(query_times)
        if op[1] == "and":
            if query_times == 2:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                ans = list(set(list1) & set(list2))
            elif query_times == 3:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                list3 = trie.search(op[4])
                ans = list(set(list1) & set(list2) & set(list3))
        elif op[1] == "or":
            if query_times == 2:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                ans = list(set(list1) | set(list2))
            elif query_times == 3:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                list3 = trie.search(op[4])
                ans = list(set(list1) | set(list2) | set(list3))
        elif op[1] == "not":
            if query_times == 2:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                ans = list(set(list1) - set(list2))
            elif query_times == 3:
                list1 = trie.search(op[0])
                list2 = trie.search(op[2])
                list3 = trie.search(op[4])
                ans = list(set(list1) - set(list2) - set(list3))
        # print(type(ans))
        outputs = []
        if len(ans) == 0:
            if count == count_lines:
                file.write('0')
            else:
                file.write('0' + '\n')
        else:
            if count == count_lines:
                file.write(','.join(str(v) for v in sorted(ans)))
            else:
                # outputs.append(','.join(str(e) for e in sorted(ans)))
                # print(outputs)
                file.write(','.join(str(v) for v in sorted(ans)) + "\n")
        count += 1
    query.close()
    file.close()
    print(time.time() - t0)
    # print(len(lines))
    # print(trie.search("美國"))
    # Please implement your algorithm below
    
    # TODO load source data, build search engine

    # TODO compute query result
  
    # TODO output result