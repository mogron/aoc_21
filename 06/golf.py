x=list(map(int,input().split(",")))
a=list(map(x.count,range(9)))
exec("a=a[1:7]+[a[7]+a[0],a[8],a[0]];"*256)
print(sum(a))
