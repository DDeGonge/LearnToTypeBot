import numpy as np
import sys


def main(filepath):
    with open(filepath, 'r') as f:
        data = np.genfromtxt(f, dtype=str, delimiter=',', skip_header=0)
    y = data[:,0]
    y_all = [int(r) for r in y]
    x = data[:, 1:]
    x = [[int(r, 16) for r in v] for v in x]
    l_all = [[int(k / 16) for k in r] for r in x]
    r_all = [[k % 16 for k in r] for r in x]

    sum_thresh = 50
    change_thresh = 13

    l_changes = [0]*3
    r_changes = [0]*3
    l_sum = [0]*3
    r_sum = [0]*3
    l_zerocnt = [0]*3
    r_zerocnt = [0]*3
    count = [0]*3

    guesses = []
    for l, r, y in zip(l_all, r_all, y_all):
        index = y
        count[index] += 1

        last = l[0]
        ldiffs = 0
        for pnt in l:
            if pnt != last:
                ldiffs += 1
            last = pnt
        l_changes[index] += ldiffs

        last = r[0]
        rdiffs = 0
        for pnt in r:
            if pnt != last:
                rdiffs += 1
            last = pnt
        r_changes[index] += rdiffs

        l_sum[index] += sum(l)
        r_sum[index] += sum(r)

        l_zerocnt[index] += sum([1 if v > 0 else 0 for v in l])
        r_zerocnt[index] += sum([1 if v > 0 else 0 for v in r])

        totaldiffs = (rdiffs + ldiffs) / 2
        totalsums = (sum(l) + sum(r)) / 2
        if totaldiffs < 7 or totalsums < 50:
            guesses.append(0)
        elif totalsums < 65:
            guesses.append(2)
        else:
            guesses.append(1)

    accuracy = 0
    for g, y in zip(guesses, y_all):
        print(g, y)
        if g == y:
            accuracy += 1

    accuracy /= len(guesses)
    print("ACCURACY:", round(100 * accuracy, 1))

    for lc, rc, ls, rs, lz, rz, c in zip(l_changes, r_changes, l_sum, r_sum, l_zerocnt, r_zerocnt, count):
        print(round(lc/c, 2), round(rc/c, 2), round(ls/c, 2), round(rs/c, 2), round(lz/c, 2), round(rz/c, 2))

if __name__=="__main__":
    main(sys.argv[1])