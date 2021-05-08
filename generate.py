import os
import sys
import json
import datetime

domain = 'http://127.0.0.1:5500/_local'
assetsRoot = 'http://127.0.0.1:5500/assets'
outputRoot = './_local'
environment = {}
templates = {}


def changeExtension(filename, ext):
    pos = filename.rindex('.')
    return filename[:pos]+ext


def safeWrite(path, data):
    pos = path.rindex('/')
    os.makedirs(path[:pos+1], exist_ok=True)
    print('write: ', path)
    open(path, 'w', encoding='utf-8').write(data)


def safeJSON(obj):
    return json.dumps(obj).replace("'", "&apos;")


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


def genTemplate(html, args):
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
        'title': filename,
        'description': '',
        'creationDate': None,
        'priority': None,
        'lang': lang
    }
    for l in lines:
        for i in info:
            if l.startswith('<!--{}:'.format(i)):
                pos = l.find(':')
                info[i] = l.strip()[pos+1:-3].strip()
    if info['priority'] == None:
        info['priority'] = info['creationDate']
    return path+filename, info


def genArticle(name, info):
    print('generate: article', name)
    args = environment.copy()
    args.update({
        'creationDate': info['creationDate'],
        'titles': safeJSON(info['titles']),
        'srcs': safeJSON(info['srcs'])
    })
    html = genTemplate('<!--template:article-->', args)
    safeWrite(outputRoot+name+'.html', html)


def aggregateArticle(versions):
    ret = {
        'creationDate': '99999999',
        'priority': ''
    }
    srcs = {}
    titles = {}
    descriptions = {}
    for path, info in versions:
        ret['creationDate'] = min(ret['creationDate'], info['creationDate'])
        ret['priority'] = max(ret['priority'], info['priority'])
        srcs[info['lang']] = path
        titles[info['lang']] = info['title']
        descriptions[info['lang']] = info['description']
    ret.update({
        'srcs': srcs,
        'titles': titles,
        'descriptions': descriptions
    })
    return ret


def genIndex(path, articles):
    print('generate: index', path)
    index = ''
    articles.sort(key=lambda a: a[1]['priority'], reverse=True)
    for a in articles:
        args = environment.copy()
        args.update({
            'path': a[0]+'.html',
            'titles': safeJSON(a[1]['titles']),
            'descriptions': safeJSON(a[1]['descriptions']),
            'creationDate': a[1]['creationDate']
        })
        index += genTemplate('<!--template:indexArticle-->', args)
    args = environment.copy()
    path2 = path
    if path2 == '/':
        path2 = "Zzzyt's Blog"
    args.update({
        'titles': safeJSON({"en": "Zzzyt's Blog: "+path}),
        'dir': path2,
        'generateIndex': index
    })
    html = genTemplate('<!--template:index-->', args)
    safeWrite(outputRoot+path+'index.html', html)


def gen(path):
    l = os.listdir('.'+path)
    print('gen: at path:', path, l)
    dirs = []
    articles = {}
    for filename in l:
        if filename.startswith('_'):
            continue
        if filename.startswith('assets'):
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
    for name in articles:
        articles[name] = aggregateArticle(articles[name])
        genArticle(name, articles[name])
    articleList = list(articles.items())
    for d in dirs:
        articleList.extend(gen(path+d[1]+'/'))
    print(articleList)
    genIndex(path, articleList)
    return articleList


def main():
    global domain
    global assetsRoot
    global environment
    global outputRoot
    if len(sys.argv) > 1:
        outputRoot = '.'
        if sys.argv[1] == 'cleanup':
            cleanup()
            return
        elif sys.argv[1] == 'remote':
            domain = 'https://z.ys.al'
            assetsRoot = domain+'/assets'
        else:
            domain = sys.argv[1]
            assetsRoot = domain+'/assets'
    environment = {
        'domain': domain,
        'assetsRoot': assetsRoot,
        'generateTime': str(datetime.datetime.utcnow())+' UTC'
    }
    print(' Environment '.center(60, '='))
    print('outputRoot:', outputRoot)
    print(environment)
    print(''.center(60, '='))
    # cleanup()
    readTemplates()
    gen('/')


if __name__ == '__main__':
    main()
