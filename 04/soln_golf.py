a,*I=open(0).readlines()
u=range
g=a.split(",")
print([[sum((1-(e in g[:i+1]))*int(e)for r in b for e in r)*int(g[i])]for i in u(len(g))for b in[[I[s+n].split()for n in u(5)]for s in u(1,len(I),6)]if any(all(e in g[:i+1] for e in r)or all(r[i]in g[:i+1] for i in u(5))for r in b)][0])
