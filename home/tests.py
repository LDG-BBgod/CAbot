from django.test import TestCase

# Create your tests here.
content = {}


test1 = ['현대','기아','삼성','몰루',]
test2 = ['1','2','3','4']
for a in test1:
    content[a] = []
    content[a].append(a)
    content[a].append({})

    for b in test2:
        content[a][1][b] = []
        content[a][1][b].append(b)
        content[a][1][b].append({})

print(content)