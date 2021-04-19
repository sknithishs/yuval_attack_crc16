import random
import string
import crc16
import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

no_message = pow(2,(16/2))

def yuval(x1, x2):
    while True:
        mx1 = getModifiedList(x1, no_message)
        hmx1 = {}
        for i in mx1:
            hmx1[str(hashCalc(i[0]))] = i 
        mx2 = getModifiedList(x2, no_message)
        for i in mx2:
            if str(hashCalc(i[0])) in hmx1:
                return [hmx1[str(hashCalc(i[0]))], i]
    return None, None

def hashCalc(m):
    return crc16.crc16xmodem(m.encode('ascii'))

def getModifiedList(m, s):
    data=[[m,0]]
    while len(data)<s:
        m = data[0][0]
        diff = random.randint(1,2)
        for i in range(diff):
            r = random.randint(0,len(m)-1)
            m = m[0:r]+random.choices(string.punctuation.replace('\\','')+string.ascii_letters+string.digits, k = 1)[0]+m[r:]
        if m not in data:
            data.append([m, diff])
    return data

def driver():
    if len(sys.argv)>2:
        legitfname = sys.argv[1]
        fraudfname = sys.argv[2]
        try:
            legitfname = sys.argv[1]
            legitfile = open(legitfname,'r')
        except:
            print("Legitimate file can't be read")
            exit(0)
        try:    
            fraudfile = open(fraudfname,'r')
        except:
            print("Fraudulent file can't be read")
            exit(0)
        legitdata = legitfile.read()
        frauddata = fraudfile.read()
    else:
        legitdata = input("Enter Legitimate Data: ")
        frauddata = input("Enter Fraudulent Data: ")
    
    print("\nLegitimate Message: "+legitdata)
    print("Hash: "+str(hex(hashCalc(legitdata))))
    print("\nFraudulent Message: "+frauddata)
    print("Hash: "+str(hex(hashCalc(frauddata))))
    modified = yuval(legitdata, frauddata)
    print("\nModified Legitimate Message: "+modified[0][0])
    print("Hash: "+str(hex(hashCalc(modified[0][0]))))
    print("\nModified Fradulent Message: "+modified[1][0])
    print("Hash: "+str(hex(hashCalc(modified[1][0]))))
    
driver()
