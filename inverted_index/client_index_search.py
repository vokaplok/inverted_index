#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, sys

if __name__ == "__main__":
    #while True:
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    res = ""
    word = input("Enter word: ")
    count_docs = input("Enter count docs: ")
    res_text = input("Receive text or not (y/n): ")
    sent_tupple = (word, count_docs, res_text)
    sock.send(str(sent_tupple).encode())
    while True:
        data = sock.recv(1024).decode()
        res = res + data
        if len(data) < 1024:
            break
    print(res)
    sock.close()
