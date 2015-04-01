#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

import ppcio

target = (('127.0.0.1', 10007))


def write_answer(io, ans):
    io.writeline(ans)

def read_question(io):
    return int(io.sock.recv(1024))

def calculate(question):
    def zhengliz(exp):
        e = 0
        while e<=101:
            if exp[e] >= 2:
                exp[e+1] += exp[e]/2
                exp[e] = exp[e]%2
            e += 1

    def zhenglif(exp):
        e = 101
        while e>=0:
            if exp[e] <= -2:
                exp[e+1] -= (-exp[e])/2
                exp[e] = -((-exp[e])%2)
            e -= 1

    def getz(goal):
        exp = [0] * 102

        n = goal
        e = 99
        while e>=0 and n!=0:
            if n - 2**e >= 0:
                # print e
                exp[e] = 1
                n -= 2**e
            e -= 1
        e = 0
        while e <=101:
            if e%2 == 1:
                if exp[e] == 1:
                    exp[e] = -1
                    exp[e+1] += 1
            zhengliz(exp)
            e += 1
        s = ''
        print exp
        e = 101
        flag = True
        while e >= 0:
            if exp[e] != 0:
                if flag:
                    s += '%d' % e
                    flag = False
                else:
                    s += ' %d' % e
            e -= 1
        return s

    def getf(goal):
        exp = [0] * 102

        n = -goal
        e = 99
        while e>=0 and n!=0:
            if n - 2**e >= 0:
                # print e
                exp[e] = -1
                n -= 2**e
            e -= 1
        print exp
        e = 0
        while e <=101:
            if e%2 == 0:
                if exp[e] == -1:
                    exp[e] = 1
                    exp[e+1] -= 1
            zhenglif(exp)
            e += 1
        s = ''
        print exp
        e = 101
        flag = True
        while e >= 0:
            if exp[e] != 0:
                if flag:
                    s += '%d' % e
                    flag = False
                else:
                    s += ' %d' % e
            e -= 1
        return s

    if question >= 0:
        ans = getz(question)
    else:
        ans = getf(question)
    return ans


level = ppcio.Level(50,calculate, read_question, write_answer, 'code200.db', 'code200')

myppcio = ppcio.PPCIO([level])
myppcio.set_io(target)
myppcio.run()