from os.path import isdir, join
from glob import iglob
from xml.etree.ElementTree import parse

# syspol reference
file_ext = '.tsk'

def get_categories():
    return ()

def get_category_efforts(categories=(), *, paths=None):
    if paths is not None:
        for path in paths:
            if isdir(path):
                for tsk in iglob(join(path, '*'+file_ext)):
                    return _tsk_file_get_category_efforts(categories, tsk)

def _tsk_file_get_category_efforts(categories, tskfp):
    doc = parse(tskfp)
    categories = tuple(categories)
    for tskcategory in doc.iterfind('category'):
        subject = tskcategory.get('subject')
        if subject not in categories:
            continue
        tskids = tuple(tskcategory.get('categorizables').split())
        print(tskids)
        yield (subject, None)
