import sqlite3
from itertools import chain
from os.path import join, dirname

SQL_SELECT_TAGS = "SELECT Name FROM Tags WHERE pid != 1"

SQL_SEARCH_TAGGED = '''\
SELECT DISTINCT ar.specificPath
             || a.relativepath
             || '/'
             || i.name
  'relpath'
FROM Tags t
  INNER JOIN ImageTags it
    ON t.id = it.tagid
  INNER JOIN Images i
    ON i.id = it.imageid
  INNER JOIN Albums a
    ON i.album = a.id
  INNER JOIN AlbumRoots ar
    ON ar.id = a.albumRoot
WHERE LOWER(t.Name) IN ({})\
'''

EXCLUDE_DIGIKAM_TAGS = set(('_Digikam_Internal_Tags_',))

def get_tags(dbfp, exclude=EXCLUDE_DIGIKAM_TAGS):
    exclude = set(exclude)
    conn = sqlite3.connect(dbfp)
    c = conn.cursor()
    tags = (set(chain.from_iterable(row for row in c.execute(SQL_SELECT_TAGS)))
        - exclude)
    return tags

def get_tagged_img_paths(dbfp, tags):
    query = SQL_SEARCH_TAGGED.format(','.join('?'*len(tags)))
    args = tags
    conn = sqlite3.connect(dbfp)
    c = conn.cursor()
    dbfp_dirname = dirname(dbfp)
    for relpath in chain.from_iterable(c.execute(query, args)):
        yield join(dbfp_dirname, relpath)
