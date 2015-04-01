#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

'''
The Star And Thank Author License (SATA)

Copyright (c) 2015 yuf4n(yufanpi@gmail.com)

Project Url: https://github.com/yufanpi/ppcio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software. 

And wait, the most important, you shall star/+1/like the project(s) in project url 
section above first, and then thank the author(s) in Copyright section. 

Here are some suggested ways:

 - Email the authors a thank-you letter, and make friends with him/her/them.
 - Report bugs or issues.
 - Tell friends what a wonderful project this is.
 - And, sure, you can just express thanks in your mind without telling the world.

Contributors of this project by forking have the option to add his/her name and 
forked project url at copyright and project url sections, but shall not delete 
or modify anything else in these two sections.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import zio
import sqlite3

class Level():
    round = 0
    __calculate = None
    __read_question = None
    __write_answer = None
    __cache_file = ''
    __cache_table = ''
    __db_cx = None

    def __init__(self, round, caluculate, read_question, write_answer, cache_file, cache_table):
        self.round = round
        self.__cache_file = cache_file
        self.__cache_table = cache_table
        self.__read_question = read_question
        self.__write_answer = write_answer
        self.__calculate = caluculate
        self.__db_init(cache_file, cache_table)

    def __db_init(self, __cache_file, __cache_table):
        self.cx = sqlite3.connect(__cache_file)
        cu = self.cx.cursor() 
        cu.execute('CREATE TABLE IF NOT EXISTS  %s (question VARCHAR(4096)  PRIMARY KEY,answer VARCHAR(4096))' % self.__cache_table)
        cu.close()

    def __db_write_record(self, question, answer):
        cu = self.cx.cursor()
        cu.execute("insert into %s values (?,?)" % self.__cache_table, (question, answer))
        self.cx.commit()
        cu.close()

    def __db_update_record(self, question, answer):
        cu = self.cx.cursor()
        cu.execute("update %s  set answer=(?) where question=(?)" % self.__cache_table, (question, answer))
        self.cx.commit()
        cu.close()

    def __db_read_record(self, question):
        cu = self.cx.cursor()
        cu.execute('select answer from %s where question=(?)' % self.__cache_table, (question,))
        result = cu.fetchone()
        if result:
            return result[0]
        else:
            return None

    def write_cache(self, question, answer):
        try:
            self.__db_write_record(question, answer)
        except sqlite3.IntegrityError:
            self.__db_update_record(question, answer)

    def read_cache(self, question):
        return self.__db_read_record(question)

    def run(self, io):
        question = self.__read_question(io)
        ans = self.read_cache(question)
        cached = True
        if not ans:
            cached = False
            ans = self.__calculate(question)
        if cached:
            pass
        self.__write_answer(io, ans)
        return question, ans


class PPCIO():
    __zio_target = None
    __zio_print_read = True
    __zio_print_write = True
    __zio_timeout = 8
    recv_welcome = None
    io = None
    level_list = []

    def __init__(self, level_list, recv_welcome = lambda io:None):
        self.level_list = level_list
        self.recv_welcome = recv_welcome

    def set_io(self, target, print_read = True, print_write = True, timeout=8):
        self.__zio_target = target
        self.__zio_print_read = print_read
        self.__zio_print_write = print_write
        self.__zio_timeout = timeout

    def run(self):
        io = zio.zio(self.__zio_target, print_read=self.__zio_print_read, print_write=self.__zio_print_write, timeout=self.__zio_timeout)
        self.recv_welcome(io)
        last_ques = ''
        last_ans = ''
        for level in self.level_list:
            for i in xrange(level.round):
                this_ques, this_ans = level.run(io)
                level.write_cache(last_ques, last_ans)
                last_ques = this_ques
                last_ans = this_ans
        io.interact()
