element_types = [{'name':'spec','parents':[]},{'name':'chunk','parents':['spec','proc']},{'name':'probe','parents':['proc']},{'name':'proc','parents':[]},{'name':'image','parents':['proc']}]

class Node(object):
    def __init__(self):
        self.name = ''
        self.left = []
        self.right = []
        self.element_type = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return '%s, left count: %s, right count %s' % (self.name, str(len(self.left)), str(len(self.right)))

root = Node()
root.name = 'project'

for element_type in element_types:
    n = Node()
    n.name = element_type['name']
    n.left.append(root)
    root.right.append(n)
    n.element_type = element_type

temp_list = root.right

for node in temp_list:
    for par_name in node.element_type['parents']:
        parent = next(iter(filter(lambda a,b=par_name: a.name==b,root.right)))
        if not parent:
            continue
        node.left.append(parent)
        if root in node.left:
            node.left.remove(root)
            if node in root.right:
                root.right.remove(node)
        parent.right.append(node)

print "root: " + root.name
print "root children: ",
for x in root.right:
  print x.name,

def printr(n):
    for child in n.right:
        print child.name
        printr(child)
    #print n.name

printr(root)

import pdb; pdb.set_trace()
