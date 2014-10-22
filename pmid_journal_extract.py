from mw import xml_dump
import datetime
import mwparserfromhell
import json
import re

files = ["enwiki-20140304-pages-articles-multistream.xml"]

stime = datetime.datetime.now()

print('starting at', stime)

valid_page_titles = json.load(open('combined_page_titles.json', 'r'))

def page_info(dump, path):
    for page in dump:
        journal_pmcs = list()
        if page.namespace == 0:
            if page.title in valid_page_titles:
                #print(page.title)
                revisions = list(page)
                latest_revision = revisions[0]
                journal_pmcs = re.findall(r"pmid\s*\=\s*(.*?)[\|\}]", latest_revision.text, flags=re.IGNORECASE)
            yield(page.title, page.id, {'journal_pmcs':journal_pmcs})
         

outfile = open('journal_pmid_list.txt', 'w')

for page_title, page_id, doi_dict in xml_dump.map(files, page_info):
    if doi_dict['journal_pmcs']:
        print(' pageid', page_id, ' page title ', page_title , ' doi_dict', doi_dict)
        for doi in doi_dict['journal_pmcs']:
            outfile.write(str(page_title) + '\t'+ str(doi) + '\n')

outfile.close()

etime = datetime.datetime.now()
print(etime)
print('took ', (etime - stime))
