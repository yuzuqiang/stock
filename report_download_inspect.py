import os
import sys
cpath = '/Volumes/ST HDD/stock/report/sh/quarter3/'
bpath = '/Volumes/ST HDD/stock/report/sh/semiannual/'
def inspect(d):
    checks = os.listdir(cpath+d[1])
    bases = os.listdir(bpath+d[1])
    codes = [item[0:6] for item in checks]
    losts = [item for item in filter(lambda x: x[0:6] not in codes, bases)]
    return losts

if __name__ == '__main__':
    print(inspect(sys.argv))
