import re
import socket
from time import sleep
s = socket.socket()
s.connect(('neverending.tuctf.com', 12345))
a=b' !"#$%+,-./0:;<=>?@aA{|}~\n'
data = s.recv(1024).decode('ascii')
while True:
    
    
    #print(data)
    s.sendall(a)
    sleep(1)
    data = s.recv(1024).decode('ascii')
    print(data)
    b=re.search('encrypted is (.+?)\n', data).group(1)
    c=re.search('is (.+?) decrypted', data).group(1)
    res=''
    alphashift=ord('a')-ord(b[a.index(b'a')])
    Alphashift=ord('A')-ord(b[a.index(b'A')])
    digshift=ord('0')-ord(b[a.index(b'0')])
    othershift=ord(':')-ord(b[a.index(b':')])
    #print(str(alphashift)+" "+str(digshift)+" "+str(othershift))
    #dbg=[]
    for i in c:
        if chr((ord(i)+alphashift)).isalpha():
            #if i.isupper():
            tmp=ord(i)+alphashift
            #else:
                #res+=chr(ord(i)+alphashift)
        #elif i.isdigit():
            #res+=chr(ord(i)+digshift)
        else:
            tmp=ord(i)+othershift
        if tmp>126:
            tmp%=95
        if tmp<32:
            tmp+=95
        res+=chr(tmp)s
        #dbg.append(tmp)
    print(res)
    #print(dbg)
    res+='\n'
    s.sendall(bytes(res, 'ascii'))
    sleep(.3)