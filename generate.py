import os
import sys
import datetime

domain = 'http://127.0.0.1:5500'
environment = {}
templates = {}


def changeExtension(filename, ext):
    pos = filename.rindex('.')
    return filename[:pos]+ext


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
        templates[i[:-5]] = open('./_template/'+i).read()


def genTemplate(html, args):
    for inf in range(100):
        for i in templates:
            flag = True
            key = '<!--template:{}-->'.format(i)
            if html.find(key) != -1:
                flag = False
                html = html.replace(key, templates[i])
        if flag:
            break
        if inf == 99:
            print('WARNING: Infinite recurvise template detected!')
    for i in args:
        html = html.replace('<!--{}-->'.format(i), args[i])
    return html


def parseArticle(path, filename):
    lines = open('.'+path+filename, encoding='utf-8').readlines()
    title = filename
    description = ''
    for l in lines:
        if l.startswith('<!--title:'):
            pos = l.find(':')
            title = l.strip()[pos+1:-3].strip()
        if l.startswith('<!--description:'):
            pos = l.find(':')
            description = l.strip()[pos+1:-3].strip()
    return path+filename, title, description


def genArticle(path, title, description):
    print('generate: article', path)
    args = environment.copy()
    args.update({
        'markdownSrc': path,
        'title': title,
        'description': description
    })
    html = genTemplate('<!--template:article-->', args)
    open('.'+changeExtension(path, '.html'), 'w', encoding='utf-8').write(html)


def genIndex(path, dirs, articles):
    index = ''
    for d in dirs:
        args = environment.copy()
        args.update({
            'path': d[0],
            'dir': d[0]+d[1]
        })
        index += genTemplate('<!--template:indexDirectory-->', args)
    for a in articles:
        args = environment.copy()
        args.update({
            'path': changeExtension(a[0], '.html'),
            'title': a[1],
            'description': a[2]
        })
        index += genTemplate('<!--template:indexArticle-->', args)
    args = environment.copy()
    path2 = path
    if path2 == '/':
        path2 = "Zzzyt's Blog"
    args.update({
        'title': "Zzzyt's Blog: "+path,
        'dir': path2,
        'generateIndex': index
    })
    html = genTemplate('<!--template:index-->', args)
    open('.'+path+'index.html', 'w', encoding='utf-8').write(html)


def gen(path):
    l = os.listdir('.'+path)
    dirs = []
    articles = []
    for filename in l:
        if filename.startswith('_template'):
            continue
        if filename.startswith('assets'):
            continue
        if filename.startswith('.git'):
            continue
        if os.path.isdir(filename):
            dirs.append((path, filename))
        else:
            if filename == 'README.md':
                continue
            if filename.endswith('.md'):
                articles.append(parseArticle(path, filename))
    for p, title, description in articles:
        genArticle(p, title, description)
    genIndex(path, dirs, articles)
    for d in dirs:
        gen(path+d[1]+'/')


def main():
    global domain
    global environment
    if len(sys.argv) > 1:
        if sys.argv[1]=='cleanup':
            cleanup()
            return
        domain = sys.argv[1]
    environment = {
        'domain': domain,
        'generateTime': str(datetime.datetime.utcnow())+' UTC'
    }
    print(' Environment '.center(60, '='))
    print(environment)
    print(''.center(60, '='))
    cleanup()
    readTemplates()
    gen('/')


if __name__ == '__main__':
    main()
