from mw import xml_dump
import datetime
from collections import defaultdict
files = ["enwiki-20140304-pages-articles-multistream.xml"]

stime = datetime.datetime.now()
print('starting at', stime)

CHARS =  ['*','#','|-','|']

def page_info(dump, path):
    for page in dump:
        if page.namespace == 0:
            revisions = list(page)
            latest_revision = revisions[0]
            lines = latest_revision.text.split('\n')
            line_starts = defaultdict(int)
            if lines[0].startswith('#REDIRECT'):
                line_starts['total'] = 9999
                #yield page.title, line_starts
                continue

            for line in lines:
                for char in CHARS:
                    if line.startswith(char):
                        line_starts[char] += 1
            
            line_starts['total'] = len(lines)
        yield page.title, line_starts

outfile = open('linestarts.txt', 'w')

outfile.write('\t'.join(['page+title', '\t'.join(CHARS), 'total', '\n']))

for page_title, line_starts in xml_dump.map(files, page_info):
    print("\t".join([page_title, str(line_starts)]))
    outfile.write(page_title+'\t')
    for char in CHARS+['total']:
        outfile.write( str(line_starts[char]) + '\t')
    outfile.write('\n')


outfile.close()
etime = datetime.datetime.now()
print(etime)
print('took ', (etime - stime))
