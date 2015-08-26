#!/usr/bin/env python
import sys
import imdb
from pymongo import MongoClient
from pymongo import ASCENDING
import csv

client = MongoClient('10.116.66.16', 27017)
db = client.face_demo
collection = db.celebrities_new
# collection.drop()
collection.create_index([("idx", ASCENDING)], unique=True)

in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
out_encoding = sys.stdout.encoding or sys.getdefaultencoding()


def main(name):
    ia = imdb.IMDb()
    name = unicode(name, in_encoding, 'replace')
    try:
        results = ia.search_person(name)
    except imdb.IMDbError, e:
        print "Probably you're not connected to Internet.  Complete error report:"
        print e
        sys.exit(3)

    if not results:
        print 'No matches for "%s", sorry.' % name.encode(out_encoding, 'replace')
        sys.exit(0)

    # Print only the first result.
    print '    Best match for "%s"' % name.encode(out_encoding, 'replace')

    # This is a Person instance.
    person = results[0]

    # So far the Person object only contains basic information like the
    # name; retrieve main information:
    ia.update(person)

    # print person.summary().encode(out_encoding, 'replace')
    res = {}
    res['Name'] = to_utf8(person.get('long imdb canonical name'))

    res['Birth_date'] = '%s (%s)' % (to_utf8(person.get('birth date')), to_utf8(person.get('birth notes')))
    res['Death_date'] = '%s (%s)' % (to_utf8(person.get('death date')), to_utf8(person.get('death notes')))

    director = person.get('director')
    if director:
        d_list = [to_utf8(x.get('long imdb canonical title'))
                    for x in director[:3]]
        res['Last_works'] = d_list
    act = person.get('actor') or person.get('actress')
    if act:
        a_list = [to_utf8(x.get('long imdb canonical title'))
                    for x in act[:5]]
        res['Last_works'] = a_list

    res['IMDb_link'] = 'http://www.imdb.com/name/nm' + person.personID
    return res


def to_utf8(data):
    if data:
        return data.encode(out_encoding, 'replace')
    else:
        return None


def mongo_insert(data):
    collection.insert(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Only one argument is required:'
        print '  %s "person list"' % sys.argv[0]
        sys.exit(2)

    person_list = sys.argv[1]
    with open(person_list, 'rb') as f:
        reader = csv.reader(f, delimiter=' ')
        person_name_list = list(reader)

    for item in person_name_list:
        name = item[0].replace('_', ' ')
        print name, item[1]
        info = main(name)
        info['idx'] = int(item[1])
        mongo_insert(info)
    client.close()
