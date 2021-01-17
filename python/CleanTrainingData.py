import sys

def main(filepath):
    output = []
    with open(filepath, 'r') as fr:
        for line in fr.readlines():
            if line not in output:
                output.append(line)

    with open(filepath+'.new', 'w+') as fw:
        fw.writelines(output)

if __name__=="__main__":
    main(sys.argv[1])