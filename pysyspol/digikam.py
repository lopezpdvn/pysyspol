import sqlite3
from itertools import chain

SQL_SELECT_TAGS = "SELECT Name FROM Tags WHERE pid != 1"
EXCLUDE_DIGIKAM_TAGS = set(('_Digikam_Internal_Tags_',))

def get_tags(dbfp, exclude=EXCLUDE_DIGIKAM_TAGS):
    exclude = set(exclude)
    conn = sqlite3.connect(dbfp)
    c = conn.cursor()
    tags = (set(chain.from_iterable(row for row in c.execute(SQL_SELECT_TAGS)))
        - exclude)
    return tags
