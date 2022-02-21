# -*- coding: utf-8 -*-
"""
Задание 11.3

Создать класс User, который представляет пользователя.
При создании экземпляра класса, как аргумент передается строка с именем пользователя.

Пример создания экземпляра класса:

In [3]: nata = User('nata')

После этого, должна быть доступна переменная username:
In [4]: nata.username
Out[4]: 'nata'

Переменная username должна быть доступна только для чтения:

In [5]: nata.username = 'user'
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-5-eba76ef1ed86> in <module>
----> 1 nata.username = 'user'

AttributeError: can't set attribute


Также в экземпляре должа быть создана переменная password, но
пока пользователь не установил пароль, при обращении к переменной должно
генерироваться исключение ValueError:

In [6]: nata.password
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-6-7527817bf03d> in <module>
----> 1 nata.password
...
ValueError: Надо установить пароль!

При установке пароля должны выполняться проверки:

* длины пароля - минимальная разрешенная длина пароля 8 символов
* содержится ли имя пользователя в пароле

Если проверки не прошли, надо вывести сообщение об ошибке и запросить пароль еще раз:
(Эта часть задания не тестируется, но ее все равно надо реализовать!)

In [7]: nata.password = 'sadf'
Пароль слишком короткий. Введите пароль еще раз: sdlkjfksnatasdfsd
Пароль содержит имя пользователя. Введите пароль еще раз: asdfkpeorti2435
Пароль установлен

Если пароль прошел проверки, должно выводиться сообщение "Пароль установлен"

In [8]: nata.password = 'sadfsadfsadf'
Пароль установлен
"""

class User:
      '''
      Класс User
      '''
      def __init__(self, username):
          self._username = username
          self._password = None
      '''
      Задаем имя
      '''
      @property
      def username(self):
          return self._username

      '''
      Чекаем наличие пароля
      '''
      @property
      def password(self):
          if self._password == None:
             raise ValueError("Надо установить пароль")
          return self._password
      
      '''
      Устанавливаем пароль через проверку
      '''
      @password.setter
      def password(self, password):
          self._password = self._check_password(password)

      '''
      Проверка пароля
      '''
      def _check_password(self, password):
          check = False
          while check == False:
                if len(password) < 8:
                   password = input('Пароль слишком короткий. Введите пароль еще раз: ')
                   check = False
                   password = password
                elif self._username in password:
                   password = input('Пароль содержит имя пользователя. Введите пароль еще раз: ')
                   check = False
                   password = password
                else: check = True
          print('Пароль установлен')
          return password

