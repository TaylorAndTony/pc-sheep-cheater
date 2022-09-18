"""
不依赖网络抓包重发的「羊了个羊」破解工具
"""
from pathlib import Path
import json

SKIP_JSON_FILESIZE = 4000


def json_matches(input: str, template: str):
    """ find whether input has same structure and data as template """
    t = template.replace('\n', '').replace('\t', '').replace(' ', '')
    t_index = 0
    for char in input:
        if char in {'\n', '\t', ' '}:
            continue
        if char != t[t_index]:
            return False
        t_index += 1
        if t_index >= len(t):
            return True
    return False


def find_users() -> list:
    users = list(Path(r'C:\Users').glob(
        '*/Documents/WeChat Files/wxid*/Applet/wx*970a9'))
    if not users:
        return []
    return users


def hack():
    paths = find_users()
    if not paths:
        print('! 没有找到微信小程序所在位置，'
              '请在微信电脑版打开「羊了个羊」并玩完第二关后关闭，再运行本程序')
        return
    if not paths[0].exists():
        print('! 内部错误：给定目录不存在')
        return
    print(f'* 修改 {paths[0]}...')
    for file in paths[0].glob("usr/gamecaches/resources/*.json"):
        filesize = file.stat().st_size
        if filesize > SKIP_JSON_FILESIZE:
            continue
        text = file.read_text('utf-8').replace('\n', '').replace('\t', '')
        if json_matches(text, '[1,0,0'):
            template = Path('local.json').read_text('utf-8')
            t_str = json.dumps(json.loads(template), indent=None)
            file.write_text(t_str, 'utf-8')
            print(f'\n+ 已修改 {file.name}')
            print(f'  源：{text[:40]}...')
            print(f'  改：{t_str[:40]}...')


if __name__ == '__main__':
    hack()
    if Path('./.noexit').exists():
        input('\n按回车键退出...')
    # print(json_matches('[0,0,0', '[0,\n0,\n0'))