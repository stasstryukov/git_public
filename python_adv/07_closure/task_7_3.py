# -*- coding: utf-8 -*-
'''
Задание 7.3

Создать функцию queue, которая работает как очередь.
После вызова функции queue, должна быть доступна возможность обращаться к
атрибутам:
* put - добавляет элемент в очередь
* get - удаляет элемент с начала очереди и возвращает None, если элементы закончились

Пример работы функции queue:

In [2]: tasks = queue()

In [3]: tasks.put('a')

In [4]: tasks.put('b')

In [5]: tasks.put('c')

In [6]: tasks.get()
Out[6]: 'a'

In [7]: tasks.get()
Out[7]: 'b'

In [8]: tasks.get()
Out[8]: 'c'

In [9]: tasks.get()

In [10]: tasks.get()
'''

def queue():
    func = []

    def put(vlan):
        nonlocal func
        func.append(vlan)

    def get():
        nonlocal func
        try:
            index = func[0]
            func.pop(0)
            return index
        except IndexError:
            return None
    queue.put = put
    queue.get = get
    return queue

