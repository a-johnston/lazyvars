pretty lazy implementation of some sort of lazy evaluation

```
from var import Session

s = Session()
s.z = s.x + s.y
s(x=5, y=3)
>> {'z': 8}
```

```
i = Variable()
i = i + 1
i = i + 1

i(0)
>> 2
i(4)
>> 6
```

```
from var import Variable

x = Variable()
y = Variable()
z = Variable()

(x + y) * z == x * z + y * z
>> True
(x + y) * z == x * z + y * z + 0
>> True
(x + y) * z == x * z + y * z * 1
>> True
(x + y) * z == x * z + y * z + 1.00000000001
>> False
```
