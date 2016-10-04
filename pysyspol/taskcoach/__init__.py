from os.path import isdir, join
from glob import iglob
from xml.etree.ElementTree import parse
from datetime import datetime, timedelta

# syspol reference
file_ext = '.tsk'

DEFAULT_TIMEDELTA = timedelta(weeks=1)
DEFAULT_DATETIME_FMT = '%Y-%m-%d %H:%M:%S'

def get_categories():
    return ()

def get_category_efforts(categories=(), *, paths=None):
    if paths is not None:
        for path in paths:
            if isdir(path):
                for tsk in iglob(join(path, '*'+file_ext)):
                    return _tsk_file_get_category_efforts(categories, tsk)

def _tsk_file_get_category_efforts(categories, tskfp):
    effort_time = timedelta()
    doc = parse(tskfp)
    categories = tuple(categories)
    for tskcategory in doc.iterfind('category'):
        subject = tskcategory.get('subject')
        if subject not in categories:
            continue
        tasks = tuple(tskcategory.get('categorizables').split())
        for task in tasks:
            #print(task)
            #print(get_task_effort(task, tskfp))
            effort_time += get_task_effort(task, tskfp)
            pass
        yield (subject, effort_time)

def get_task_effort(tskid, tskfp, start=None, end=None):
    effort_time = timedelta()
    if start is None:
        start = datetime.now() - DEFAULT_TIMEDELTA

    doc = parse(tskfp)
    task = None
    for tsktask in doc.iterfind('task'):
        if tsktask.get('id') == tskid:
            task = tsktask
            break
    if task is None:
        return effort_time

    #print('Task `{}`'.format(task.get('subject')))

    for effort in task.iterfind('effort'):
        try:
            effort_start = datetime.strptime(effort.get('start'),
                    DEFAULT_DATETIME_FMT)
            effort_end = datetime.strptime(effort.get('stop'),
                    DEFAULT_DATETIME_FMT)
        except TypeError:
            print('Effort id `{}` has no stop attribute'.format(effort.get('id')))
            continue
        if effort_start.date() < start.date():
            continue
        if end is not None and effort_end.date() > end.date():
            continue
        effort_time += effort_end - effort_start

    return effort_time
