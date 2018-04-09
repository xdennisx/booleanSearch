# booleanSearch
---
## I use two method to implement this project
- jieba & inverted index
- Brute-force method

## jieba & inverted index (inverted.py)
First use `jieba.lcut` to cut words in each line, if the result length of word is shorter 
than **3**, I'll concate the character besides it until the length is longer than **3**
```python=91
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
```
`trie.insert` is to build a `trie-tree` and `trie.search` is to find the word in tree
## Brute-force (main.py)
Read every line in **query.txt**, if find query in line then append to the list.
```python=38
for x in lines:
        op = re.split(' |\n',x)
        query_times = len(op) / 2
        list1 = search(op[0])
        list2 = search(op[2])
        if op[1] == "and":
            ans = list(set(list1) & set(list2))
            if query_times == 3:
                list3 = search(op[4])
                ans = list(set(ans) & set(list3))
        elif op[1] == "or":
            ans = list(set(list1) | set(list2))
            if query_times == 3:
                list3 = search(op[4])
                ans = list(set(ans) | set(list3))
        elif op[1] == "not":
            ans = list(set(list1) - set(list2))
            if query_times == 3:
                list3 = search(op[4])
                ans = list(set(ans) - set(list3))
        
        if len(ans) == 0:
            file.write('0')
            if count != count_lines:
                file.write('\n')
        else:
            file.write(','.join(str(v) for v in sorted(ans, key=int)))
            if count != count_lines:
                file.write("\n")
        count += 1
```
## Result Compare
| method | time |
| ------ | ----------- |
| jieba & inverted index | Brute-force |
| 29 | 0.29 |
