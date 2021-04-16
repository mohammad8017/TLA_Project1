test = {}

lst = ['q0','q1','a']

test.setdefault((lst[0],lst[2]), set()).add(lst[1])
print(test)