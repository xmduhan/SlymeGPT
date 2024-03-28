import re
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print('Use: flygpt prompt_file')
        return
    filename = sys.argv[1]
    text = Path(filename).read_text()
    line_parser = re.compile(r'(\S+)\s*:\s*(\S.*)')
    for line in text.split('\n'):
        found = line_parser.findall(line)
        if found:
            # print(found)
            cmd, args = found[0]
            print(cmd, args)

if __name__ == '__main__':
    main()
