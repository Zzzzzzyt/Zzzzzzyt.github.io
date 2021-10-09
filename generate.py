import os
import sys
import json
import datetime
import hashlib
import base64
import shutil

domain = 'http://127.0.0.1:5500/_local'
assetsRoot = 'http://127.0.0.1:5500/assets'
outputRoot = './_local'
environment = {}
templates = {}
oldIndex = {}


def changeExtension(filename, ext):
    pos = filename.rindex('.')
    return filename[:pos]+ext


def safeWrite(path, data):
    pos = path.rindex('/')
    os.makedirs(path[:pos+1], exist_ok=True)
    print('write: ', path)
    open(path, 'w', encoding='utf-8').write(data)


def htmlEncode(s):
    return s.replace('&', '&amp;').replace("'", '&apos;').replace('"', '&#39;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')


def base64Encode(s):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def miniJSON(obj):
    return json.dumps(obj, separators=(',', ':'))


def safeJSON(obj):
    return htmlEncode(miniJSON(obj))


def cleanup():
    l = os.walk('.')
    for root, dirs, files in l:
        root = root.replace(os.sep, '/')
        if root.startswith('./_template'):
            continue
        if root.startswith('./assets'):
            continue
        if root.startswith('./.git'):
            continue
        for f in files:
            if f.endswith('.html'):
                print('cleanup: remove', root+'/'+f)
                os.remove(root+'/'+f)


def readTemplates():
    l = os.listdir('./_template/')
    for i in l:
        templates[i[:-5]] = open('./_template/'+i, encoding='utf-8').read()


def genTemplate(html, args={}):
    args['args'] = base64Encode(miniJSON(args))
    for inf in range(100):
        flag = True
        for i in templates:
            key = '<!--template:{}-->'.format(i)
            if html.find(key) != -1:
                flag = False
                html = html.replace(key, templates[i])
        if flag:
            break
        if inf == 99:
            print('WARNING: Infinite recurvise template detected!')
    for i in args:
        tmp = args[i]
        if tmp == None:
            tmp = ''
        html = html.replace('<!--{}-->'.format(i), tmp)
    return html


def parseArticle(path, filename, lang):
    lines = open('.'+path+filename, encoding='utf-8').readlines()
    info = {
        'path': path+filename,
        'title': filename,
        'description': '',
        'creationDate': None,
        'priority': None,
        'lang': lang
    }
    index = -1
    for i in range(len(lines)):
        if lines[i].startswith('<!--info:'):
            index = i
    if index != -1:
        index += 1
        tmp = '{'
        while index < len(lines):
            s = lines[index]
            if s.startswith('-->'):
                break
            tmp += s[:-1]+','
            index += 1
        tmp = tmp[:-1] + '}'
        info.update(json.loads(tmp))
    if info['priority'] == None:
        info['priority'] = info['creationDate']
    return info


def genArticle(name, info):
    print('generate: article', name)
    filename = outputRoot+name+'.html'
    # flag = True
    # if name in oldIndex:
    #     for lang in info['versions']:
    #         if not(lang in oldIndex[name]['versions']
    #                and oldIndex[name]['versions'][lang]['hash'] == info['versions'][lang]['hash']):
    #             flag = False
    # if flag and os.path.exists(filename):
    #     print('skipped')
    #     return
    args = environment.copy()
    titles = {}
    srcs = {}
    for i in info['versions']:
        titles[i] = htmlEncode(info['versions'][i]['title'])
        srcs[i] = info['versions'][i]['path']
    args.update({
        'creationDate': info['creationDate'],
        'titles': base64Encode(miniJSON(titles)),
        'srcs': base64Encode(miniJSON(srcs)),
    })
    html = genTemplate('<!--template:article-->', args)
    safeWrite(filename, html)


def aggregateArticle(versions):
    ret = {
        'creationDate': '99999999',
        'priority': '',
        'versions': {}
    }
    for info in versions:
        ret['creationDate'] = min(ret['creationDate'], info['creationDate'])
        ret['priority'] = max(ret['priority'], info['priority'])
        ret['versions'][info['lang']] = {
            'title': info['title'],
            'description': info['description'],
            'path': info['path'],
            'hash': hashlib.sha256(open('.'+info['path'], 'rb').read()).hexdigest(),
        }
    return ret


def gen(path):
    l = os.listdir('.'+path)
    # print('gen: at path:', path, l)
    dirs = []
    articles = {}
    for filename in l:
        if filename.startswith('_'):
            continue
        if filename == 'assets':
            continue
        if filename.startswith('.'):
            continue
        if os.path.isdir('.'+path+filename):
            dirs.append((path, filename))
        else:
            if filename == 'README.md':
                continue
            if filename.endswith('.md'):
                name, lang = filename.split('.')[0].split('_')
                name = path+name
                if not name in articles:
                    articles[name] = []
                articles[name].append(parseArticle(path, filename, lang))
    # print(articles)
    for name in articles:
        articles[name] = aggregateArticle(articles[name])
        genArticle(name, articles[name])
    for d in dirs:
        articles.update(gen(path+d[1]+'/'))
    return articles


def genIndex(filename, titles, filter):
    args = environment.copy()
    for i in titles:
        titles[i] = htmlEncode(titles[i])
    args.update({'filterCode': filter, 'titles': base64Encode(miniJSON(titles))})
    safeWrite(outputRoot+filename, genTemplate('<!--template:index-->', args))


def main():
    global domain
    global assetsRoot
    global environment
    global outputRoot
    global oldIndex
    if len(sys.argv) > 1:
        outputRoot = '.'
        if sys.argv[1] == 'cleanup':
            cleanup()
            return
        elif sys.argv[1] == 'remote':
            domain = 'https://Zzzzzzyt.github.io'
            assetsRoot = domain+'/assets'
        else:
            domain = sys.argv[1]
            assetsRoot = domain+'/assets'
    environment = {
        'domain': domain,
        'assetsRoot': assetsRoot,
        'generateTime': str(datetime.datetime.utcnow())+' UTC'
    }
    if os.path.exists(outputRoot+'/index.json'):
        oldIndex = json.load(open(outputRoot+'/index.json'))
    print(' Environment '.center(60, '='))
    print('outputRoot:', outputRoot)
    print(environment)
    print(''.center(60, '='))
    readTemplates()
    if outputRoot != '.':
        for i in os.listdir('.'):
            if not i.startswith('_') and not i.startswith('.') and i != 'assets' and i != 'generate.py':
                dst = outputRoot+'/'+i
                print('copy: ./'+i+' to '+dst)
                if os.path.isdir(i):
                    shutil.copytree(i, dst, dirs_exist_ok=True)
                else:
                    shutil.copyfile(i, dst)
    articles = gen('/')
    safeWrite(outputRoot+'/index.json', json.dumps(articles, separators=(',', ':')))
    genIndex('/index.html', {'en': "Zzzyt's Blog"}, '')
    genIndex('/misc.html', {'en': "Zzzyt's Blog: Misc"}, 'if(!i[0].startsWith("/misc"))continue;')
    genIndex('/oi.html', {'en': "Zzzyt's Blog: OI"}, 'if(!i[0].startsWith("/oi"))continue;')


if __name__ == '__main__':
    main()
