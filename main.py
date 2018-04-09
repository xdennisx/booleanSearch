import csv
import re
import time

src = {}

def search(query):
    index = [index for index, value in src.items() if query in value]
    return index
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
    with open(args.source, newline='\n', encoding = 'utf-8') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            src[row[0]] = row[1]
    t1 = time.time() - t0
    print(t1)
    query = open(args.query, "r", encoding="UTF-8")
    lines = query.readlines()
    file = open(args.output, 'w')
    count = 1
    count_lines = len(lines)
    for x in lines:
        op = re.split(' |\n',x)
        query_times = len(op) / 2
        if op[1] == "and":
            if query_times == 2:
                list1 = search(op[0])
                list2 = search(op[2])
                ans = list(set(list1) & set(list2))
            elif query_times == 3:
                list1 = search(op[0])
                list2 = search(op[2])
                list3 = search(op[4])
                ans = list(set(list1) & set(list2) & set(list3))
        elif op[1] == "or":
            if query_times == 2:
                list1 = search(op[0])
                list2 = search(op[2])
                ans = list(set(list1) | set(list2))
            elif query_times == 3:
                list1 = search(op[0])
                list2 = search(op[2])
                list3 = search(op[4])
                ans = list(set(list1) | set(list2) | set(list3))
        elif op[1] == "not":
            if query_times == 2:
                list1 = search(op[0])
                list2 = search(op[2])
                ans = list(set(list1) - set(list2))
            elif query_times == 3:
                list1 = search(op[0])
                list2 = search(op[2])
                list3 = search(op[4])
                ans = list(set(list1) - set(list2) - set(list3))
        outputs = []
        if len(ans) == 0:
            if count == count_lines:
                file.write('0')
            else:
                file.write('0' + '\n')
        else:
            if count == count_lines:
                file.write(','.join(str(v) for v in sorted(ans, key=int)))
            else:
                file.write(','.join(str(v) for v in sorted(ans, key=int)) + "\n")
        count += 1
    query.close()
    file.close()
    print(time.time() - t0)