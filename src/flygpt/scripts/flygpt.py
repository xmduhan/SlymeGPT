import re
import sys
import subprocess
from pathlib import Path
from textwrap import dedent
from flygpt.flygpt import FlyGPTClient
from bs4 import BeautifulSoup
from termcolor import colored  # Added termcolor for colored output
from datetime import datetime

line_pattern = re.compile(r'(\S+)\s*:\s*(\S*.*\S+)')

def extract_output_files(text):
    output_files = []
    for line in text.split('\n'):
        # Split the line into command and arguments
        cmd, _, args = line.partition(':')
        cmd = cmd.rstrip()  # Remove leading and trailing whitespace
        if cmd in ('w', 'rw', 'wr'):
            output_files.append(args.strip())
    return output_files

def build_prompt(text):
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader('src/flygpt/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('default.j2')
    output_files = extract_output_files(text)
    prompt_text = template.render(human_input=generate_human_input(text), output_files=output_files)
    return prompt_text

def generate_human_input(text):
    human_input = ''
    for line in text.split('\n'):

        if '#' in line:
            line = line.split('#', 1)[0] + '\n'
            if len(line.strip()) == 0:
                continue

        if line.startswith(('sh:', 'w:', 'r:', 'rw:', 'wr:')):
            cmd, args = line.split(':', 1)
            if cmd == 'sh':
                human_input += f'```{args.strip()}\n'
                human_input += execute_shell_command(args.strip())
                human_input += '```\n\n'
            elif 'r' in  cmd:
                human_input += f'```{args.strip()}\n'
                with open(args.strip(), 'r') as f:
                    human_input += f.read() + '\n'
                human_input += f'```\n\n'
        else:
            human_input += line + '\n'
    return human_input

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
    # print(prompt_text)
    # return

    # 调用GPT
    content = []
    client = FlyGPTClient()
    print('🤖 AI正在思考中: ', end='', flush=True)  # Disable print buffer
    for chunk in client.generate(prompt_text):
        content.append(chunk)
        if chunk == '.':
            print(chunk, end='', flush=True)  # Disable print buffer
    response = content[-1]
    # print(response)
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

    # 保存发送的prompt_text和收到的response到'.prompt/.history'文件中
    prompt_history = f'''
    [{datetime.now()}] send: >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    {prompt_text}
    [{datetime.now()}] recv: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    {response}
    '''
    with open('.prompt/.history', 'a') as history_file:
        history_file.write(dedent(prompt_history))

if __name__ == '__main__':
    main()

