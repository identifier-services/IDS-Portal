def print_ascii_graph(R):
  V=list(set(R)-{','})   

  T=[' ']*40
  for e in R.split():
    x,y=sorted(map(V.index,e[::2]))
    print(*T[:x]+["+"+"--"*(y-x-1)+"-+"]+T[y+1:])
    T[x]=T[y]="|"
    print(*T)
  print(*V)

print_ascii_graph('S,C C,P R,P P,I I,D')
