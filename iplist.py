ip="172.16.143."
with open('ip.txt','w') as f:
    for i in range(122, 140):
        ip1=ip+str(i)
        f.write(ip1+'\n')
