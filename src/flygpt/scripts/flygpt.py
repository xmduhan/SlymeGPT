#!python
import re
import sys
import subprocess
from pathlib import Path
from textwrap import dedent
from flygpt.flygpt import FlyGPTClient
from bs4 import BeautifulSoup
from termcolor import colored  # Added termcolor for colored output

line_pattern = re.compile(r'(\S+)\s*:\s*(\S*.*\S+)')

def extract_output_files(text):
    output_files = []
    for line in text.split('\n'):
        # Split the line into command and arguments
        cmd, _, args = line.partition(':')
        cmd = cmd.strip()  # Remove leading and trailing whitespace
        if cmd in ('w', 'rw', 'wr'):
            output_files.append(args.strip())
    return output_files

def build_prompt(text):
    human_input = ''
    for line in text.split('\n'):
        if line.startswith(('sh:', 'w:', 'r:', 'rw:', 'wr:')):
            cmd, args = line.split(':', 1)
            print(cmd, args)
            if cmd == 'sh':
                human_input += f'```\n'
                human_input += execute_shell_command(args.strip())
                human_input += '```\n\n'
            elif 'r' in  cmd:
                print(cmd, args)
                with open(args.strip(), 'r') as f:
                    human_input += f.read() + '\n'
            elif '#' in cmd:
                # Handle single-line comment
                human_input += line.split('#', 1)[0] + '\n'
        else:
            human_input += line + '\n'

    prompt_text = dedent(f'''\
        系统: 你是一个程序员,请协助用户要求编写或修改代码.
        系统: 你的输出代码全文并无需提供其他信息.
        系统: 本次需要你提供的文件包括: { ','.join(extract_output_files(text)) }
        系统: 代码输出格式如下:
        ```文件路径
        代码内容
        ```
        以下信息由用户提供:

        ''') + human_input
    return prompt_text

def execute_shell_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def check_unpushed_commits():
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    return 'M' in result.stdout or 'A' in result.stdout or 'D' in result.stdout or 'R' in result.stdout

def push_changes():
    subprocess.run("git push origin HEAD", shell=True)

def main():
    if len(sys.argv) != 2:
        print('Usage: flygpt prompt_file')
        return

    # 生成 prompt
    text = Path(sys.argv[1]).read_text()
    prompt_text = build_prompt(text)

    # 调用GPT
    content = []
    client = FlyGPTClient()
    print('🤖 AI正在思考中: ', end='', flush=True)  # Disable print buffer
    for chunk in client.generate(prompt_text):
        content.append(chunk)
        if chunk == '.':
            print(chunk, end='', flush=True)  # Disable print buffer
    response = content[-1]
    print('💡', flush=True)  # AI思考结束后打印一个emoji灯泡图标

    # 读取返回结果并写回文件
    soup = BeautifulSoup(response, features="html.parser")
    output_files = extract_output_files(text)
    for filename in output_files:
        print(filename, end=' ... ', flush=True)  # Disable print buffer
        found = soup.find_all("code", {"class": f"language-{filename}"})
        if found:
            code_text = found[0].text
            Path(filename).write_text(code_text)
            print(colored('(OK)', 'green'), flush=True)  # Disable print buffer
        else:
            print(colored('(MISS)', 'red'), flush=True)  # Disable print buffer

    # 执行 vi +'G difftool -y' 命令前检查是否有未暂存的更改
    if check_unpushed_commits():
        subprocess.run("vi +'G difftool -y'", shell=True)
    else:
        print('没有未暂存的更改，无需执行difftool。')

    # 检查工作区是否有未推送的提交
    if check_unpushed_commits():
        # 提示用户是否需要推送
        push = input("是否需要推送本地提交至远程仓库？(y/n): ")
        if push.lower() == 'y':
            push_changes()

if __name__ == '__main__':
    main()
