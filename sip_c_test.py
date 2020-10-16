
import sys
from sipClient import simpleSipClient

client=simpleSipClient()
print client.getSelfURI()


while True:
    print "c-Call \r\nh-Hang Up \r\nq-Exit\r\nenter command:"
    command=sys.stdin.readline().rstrip("\r\n")
    if command=="c":
        client.make_call("sip:1001@172.17.10.71")
    elif command=="h":
        client.hang()
    elif command=="q":
        break

print "Destroyed"