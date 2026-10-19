# rough knapsack over Main Prompt clauses: (id, cost chars, value, mandatory)
cl = [
('a1',52,10,1),('a2',18,8,1),
('b1',77,10,1),   # CP body w/o label
('c1',60,8,1),('c2',28,9,1),('c3',35,5,0),
('d1',11,4,0),('d2',50,7,1),('d3',33,6,0),
('e1',37,8,1),('e2',54,7,1),('e3',42,5,0),
('f1',58,9,1),('f1b',24,6,0),('f2',19,4,0),('f3',47,8,1),('f3b',25,4,0),('f4',33,8,1),('f5',50,3,0),('f6',39,4,0),
('g1',86,10,1),('g1b',37,3,0),('g2',33,8,1),('g3',95,8,1),('g4',82,9,1),('g5',84,5,0),('g6',38,3,0),('g7',40,4,0),('g8',16,2,0),('g9',62,7,1),('g9b',36,3,0),
('h1',92,8,1),('h2',57,4,0),('h3',49,7,0),
('i1',25,6,1),('i2',80,5,0),('i3',40,5,0),('i4',59,5,0),('i5',30,3,0),('i6',52,5,0),
('j1',72,7,1),('j2',82,7,1),('j3',29,4,0),
('k1',36,4,0),('k2',84,7,1),('k3',54,5,0),('k3b',38,4,0),
]
labels=143+10
budget=1040-labels
mand=sum(c for _,c,_,m in cl if m)
print('mandatory cost',mand,'budget',budget)
opt=[x for x in cl if not x[3]]
opt.sort(key=lambda x:-x[2]/x[1])
rem=budget-mand
chosen=[]
for i,c,v,m in opt:
    if c<=rem:
        chosen.append(i); rem-=c
print('chosen optional',chosen,'remaining',rem)
print('dropped',[i for i,c,v,m in opt if i not in chosen])
print('total cost all',sum(c for _,c,_,_ in cl))
