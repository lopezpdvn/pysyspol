import sys
from os.path import isdir, join
from glob import iglob
from xml.etree.ElementTree import parse
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

# syspol reference
file_ext = '.tsk'

DEFAULT_TIMEDELTA = timedelta(weeks=1)
DEFAULT_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

def get_categories():
    return ()

def get_category_efforts(categories=(), start=None, end=None, *, paths=None):
    if start is None:
        start = datetime.now() - DEFAULT_TIMEDELTA

    if paths is not None:
        for path in paths:
            if isdir(path):
                for tsk in iglob(join(path, '*'+file_ext)):
                    yield from _tsk_file_get_category_efforts(categories, tsk,
                            start, end)

def plot_category_efforts(data, fnames=()):
    if not len(fnames):
        return
    categories = tuple(record[0] for record in data)
    effort = tuple(record[1] for record in data)
    plt.pie(effort, labels=categories, shadow=True)
    plt.axis('equal')
    for fname in fnames:
        plt.savefig(fname)

def _tsk_file_get_category_efforts(categories, tskfp, start, end):
    doc = parse(tskfp)
    categories = tuple(categories)
    for tskcategory in doc.iterfind('.//category'):
        effort_time = timedelta()
        subject = tskcategory.get('subject')
        if subject not in categories:
            continue
        tasks = tuple(tskcategory.get('categorizables').split())
        for task in tasks:
            effort_time += get_task_effort(task, tskfp, start, end)
        yield (subject, effort_time.total_seconds())

def get_task_effort(tskid, tskfp, start, end=None):
    effort_time = timedelta()
    doc = parse(tskfp)
    task = doc.find(".//task[@id='{}']".format(tskid))
    if task is None:
        return effort_time

    for effort in task.iterfind('effort'):
        try:
            effort_start = datetime.strptime(effort.get('start'),
                    DEFAULT_DATETIME_FMT)
            effort_end = datetime.strptime(effort.get('stop'),
                    DEFAULT_DATETIME_FMT)
        except TypeError:
            #print('Effort id `{}` has no stop attribute'.format(
                #effort.get('id')), file=sys.stderr)
            continue
        if effort_start < start:
            continue
        if end is not None and effort_end > end:
            continue
        effort_time += effort_end - effort_start

    return effort_time
