q = []

q.append('table1.field1 == value1')
q.append('table1.field1 = value1')
q.append('table1.field1 != value1')
q.append('table1.field1 <> value1')

q.append('table1.field1 = value1 AND table2.field2 = value2')
q.append('table1.field1 = value1 OR table2.field2 = value2')

q.append('table1.field1 = value1 AND table2.field2 = value2 AND table3.field3 = value3')
q.append('table1.field1 = value1 OR table2.field2 = value2 OR table3.field3 = value3')
q.append('table1.field1 = value1 AND table2.field2 = value2 OR table3.field3 = value3')
q.append('table1.field1 = value1 OR table2.field2 = value2 AND table3.field3 = value3')

q.append('table1.field1 != value1 AND table2.field2 = value2')
q.append('table1.field1 = value1 AND table2.field2 != value2')

q.append('table1.field1 != value1 OR table2.field2 = value2')
q.append('table1.field1 = value1 OR table2.field2 != value2')

q.append('table1.field1 != value1 AND table2.field2 = value2 AND table3.field3 = value3')
q.append('table1.field1 != value1 OR table2.field2 = value2 OR table3.field3 = value3')

q.append('table1.field1 = value1 AND table2.field2 != value2 AND table3.field3 = value3')
q.append('table1.field1 = value1 OR table2.field2 != value2 OR table3.field3 = value3')

q.append('table1.field1 != value1 AND table2.field2 = value2 OR table3.field3 = value3')
q.append('table1.field1 != value1 OR table2.field2 = value2 AND table3.field3 = value3')

q.append('table1.field1 = value1 AND table2.field2 != value2 OR table3.field3 = value3')
q.append('table1.field1 = value1 OR table2.field2 != value2 AND table3.field3 = value3')

def token_string(query):
    return query.replace('==','=').replace('!=','#').replace('<>','#')\
        .replace(' = ','=').replace(' # ','#')\
        .replace('(','').replace(')','')\
        .replace('=','(=)').replace('#','(#)')\
        .replace('&&','AND').replace('||','OR')\
        .replace('&','AND').replace('|','OR')\
        .replace(' and ', ' AND ').replace(' or ', ' OR ')\
        .replace(' AND ', '<AND>').replace(' OR ', '<OR>')\
        .replace(', ',',').replace(' ,',',')\
        .replace('. ','.'.replace(' .','.'))

symbols = ['>','<',')','(','.',]

def foo(query_parts, symbols):
    for symbol in symbols:
        temp_parts =  []
        for part in query_parts:
            temp_parts.extend(part.split(symbol))
        query_parts = temp_parts
    return query_parts

from collections import namedtuple

Term = namedtuple('Term', ['table','field','operator','value'])

def bar(parts):
    print parts
    terms = []
    operators = []
    while len(parts) >= 4:
        terms.append(Term(*parts[:4]))
        parts = parts[4:]
        if parts:
            operators.append(parts[0])
            parts = parts[1:]
    print terms
    print operators

for query in q:
    print
    print "-=-=-=-"
    print
    print query

    query = token_string(query)
    print bar(foo([query], symbols))


