import re
import sys
import getopt
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

useage = 'python index.py -u <url>'


# 获取命令行参数
def getArgs(argv):
    if len(argv) == 0:
        print(useage)
        sys.exit(2)
    url = ''
    try:
        opts, args = getopt.getopt(argv, "hu:", ["url="])
    except getopt.GetoptError:
        print(useage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(useage)
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
    return {
        'url': url,
    }

# 获取真实地址
def getRealUrl(url):
    parse = urlparse(url)
    host = parse.netloc
    if 'bilibili.com' not in host:
        print('url host wrong, ' + url)
    path = parse.path
    scheme = parse.scheme
    headers = {
        'authority': host,
        'method': 'GET',
        'path': path,
        'scheme': scheme,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Mobile Safari/537.36',
    }
    res = requests.get(url=url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html5lib')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'readyVideoUrl:' in str(script):
            search = re.search('readyVideoUrl: \'[\w\W]*\',', str(script))
            group = search.group()
            return scheme + ':' + group[len('readyVideoUrl: \''):len(group) - 2]


def main(argv):
    args = getArgs(argv)
    url = args['url']
    realUrl = getRealUrl(url)
    print(realUrl)


if __name__ == "__main__":
    main(sys.argv[1:])
