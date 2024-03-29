import re
import sys
import subprocess
from pathlib import Path
from textwrap import dedent
from flygpt.flygpt import FlyGPTClient
from bs4 import BeautifulSoup

line_pattern = re.compile(r'(\S+)\s*:\s*(\S*.*\S+)')

def extract_output_files(text):
    output_files = []
    for (cmd, args) in line_pattern.findall(text):
        if 'w' in cmd:
            output_files.append(args)
    return output_files

def build_prompt(text):
    human_input = ''
    for (cmd, args) in line_pattern.findall(text):
        if cmd == 'p':
            human_input += args + '\n'
        elif cmd == 'sh':
            human_input += f'```\n'
            human_input += execute_shell_command(args)
            human_input += '```\n\n'

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
        return result.std
