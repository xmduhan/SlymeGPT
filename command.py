import re
import sys
from pathlib import Path
from glob import glob
from textwrap import dedent
from flygpt.flygpt import FlyGPTClient
from bs4 import BeautifulSoup

line_parser = re.compile(r'(\S+)\s*:\s*(\S*.*\S+)')

def get_output_files(text):
    output_files = []
    for (cmd, args) in line_parser.findall(text):
        if 'w' in cmd:
            output_files.append(args)
    return output_files

def build_prompt(text):
    human_input = ''
    for (cmd, args) in line_parser.findall(text):
        if cmd == 'l':
            human_input += f'```ls {args}:\n'
            human_input += '\n'.join(glob(args)) + '\n'
            human_input += '```\n\n'
        if 'r' in cmd:
            human_input += f'```{args}\n'
            human_input += Path(args).read_text()
            human_input += '```\n\n'
        if cmd == 'p':
            human_input += args + '\n'

    prompt_text = dedent(f'''\
        系统: 你是一个程序员,请协助用户要求编写或修改代码.
        系统: 你的输出代码全文并无需提供其他信息.
        系统: 本次需要你提供的文件包括: { ','.join(get_output_files(text)) }
        系统: 代码输出格式如下:
        ```文件路径
        代码内容
        ```
        以下信息由用户提供:

        ''') + human_input
    return prompt_text

def main():
    if len(sys.argv) != 2:
        print('Use: flygpt prompt_file')
        return

    # 生成 prompt
    text = Path(sys.argv[1]).read_text()
    prompt_text = build_prompt(text)

    # 调用GPT
    content = []
    client = FlyGPTClient()
    print('AI正在思考中: ', end='') 
    for chunk in client.generate(prompt_text):
        content.append(chunk)
        if chunk == '.':
            print(chunk, end='')
    response = content[-1]
    print('')

    # 读取返回结果并写回文件
    soup = BeautifulSoup(response, features="html.parser")
    output_files = get_output_files(text)
    for filename in output_files:
        print(filename, end=' ... ')
        found = soup.find_all("code", {"class": f"language-{filename}"})
        if found:
            code_text = found[0].text
            Path(filename).write_text(code_text)
            print('(OK)')
        else:
            print('(MISS)')

if __name__ == '__main__':
    main()
