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

def stuff(query):
    print query

for query in q:
    stuff(query)

print

s = 'a.b = c AND d.e = f OR g.h = i AND j.k = l'
s = 'a.b == c AND d.e = f OR g.h != i AND j.k <> l'

s=s.replace('==','=').replace('!=','#').replace('<>','#')
s=s.replace('(','').replace(')','')
s=s.replace(' = ','=').replace(' # ','#')
s=s.replace('=','(=)').replace('#','(#)')
s=s.replace('&&','AND').replace('||','OR').replace('&','AND').replace('|','OR')
s=s.replace(' and ', ' AND ').replace(' or ', ' OR ')
s=s.replace(' AND ', '<AND>').replace(' OR ', '<OR>')

print s
print

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

def token_list_(token_string):
    print '-=-=dd-=-=-=-'
    print
    tokens = token_string.split('>')
    print tokens
    print [x[1] for x in tokens if len(x) == 2]
    print
    tokens = [x.split('<') for x in tokens]
    print tokens
    print [x[1] for x in tokens if len(x) == 2]
    print
    tokens = [x[0].split(')') for x in tokens]
    print tokens
    print [x[1] for x in tokens if len(x) == 2]
    print
    tokens = [x[0].split('(') for x in tokens]
    print tokens
    print [x[1] for x in tokens if len(x) == 2]
    print
    tokens = [x[0].split('.') for x in tokens]
    print tokens
    print [x[1] for x in tokens if len(x) == 2]
    print
    tokens = [x[0] for x in tokens]
    return tokens

for qry in q:
    t_s = token_string(qry)
    print t_s
    print
    print token_list_(t_s)
    print

def token_list__(token_string, symbols):
    tokens = token_string.split('>')
    tokens = [x.split('<') for x in tokens]
    tokens = [x[0].split(')') for x in tokens]
    tokens = [x[0].split('(') for x in tokens]
    tokens = [x[0].split('.') for x in tokens]
    tokens = [x[0] for x in tokens]
    return tokens

def token_list(token_string, symbols):
    left = [token_string]
    right = []
    for symbol in symbols:
        print
        print left
        if not left:
            break
        if isinstance(next(iter(left),None), list):
            left = [x[0].split(symbol) for x in left]
        else:
            left = [x.split(symbol) for x in left]
    while True:
        left = left[0]
        if not isinstance(left, list):
            break
    return left

print '==========='

symbols = ['>','<',')','(','.',]
for qry in q:
    # print qry
    print token_list(token_string(qry), symbols)
    
