import math
import sys
import random


#Data Bug
Seed = ""
def randomWord(len):
    chrs = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    word = ""
    for i in range(len):
        word+=random.choice(chrs)
    return(word)
def SrandomWord(len):
    chrs = ['A','A','A','B','C','D','E','E','E','E','E','E','F','G','H','I','I','I','I','J','K','L','M','N','O','O','O','P','Q','R','S','T','U','U','U','V','W','X','Y','Z']
    word = ""
    for i in range(len):
        word+=random.choice(chrs)
    return(word)
def scatterWord(str):
    string = str
    newstring = ""
    cis = list(range(0,len(string)))
    random.shuffle(cis)
    for i in cis:
        newstring+=string[i]
    return(newstring)


while Seed != "!STOP":
    print("Hello World, I am DATABUG, I generate Data from numbers and words,\nenter literally anything and I'll try to process it into way too much information. Enter !STOP to end session.")
    Seed = input(">>>")
    Orde = 0
    for chr in list(Seed):
        Orde+=ord(chr)

    try:
        random.seed(int(Seed))
        print("ord:"+str(Orde))
        print("int:"+str(int(Seed)))
        print("abs:"+str(abs(Seed)))
        print("hlf:"+str(int(Seed)/2))
        print("len:"+str(len(Seed)))
        print("rnt:"+str(random.randint(1,int(Seed))))
        print("rnr:"+str(random.random()))
        print("rwd:"+str(randomWord(len(Seed))))
        print("srw:"+str(SrandomWord(len(Seed))))
        print("scw:"+scatterWord(Seed))

    except:
        random.seed(Orde)
        print("ord:"+str(Orde))
        print("int:"+str(int(Orde)))
        print("abs:"+str(abs(Orde)))
        print("hlf:"+str(Orde/2))
        print("len:"+str(len(Seed)))
        print("rnt:"+str(random.randint(1,Orde)))
        print("rnr:"+str(random.random()))
        print("rwd:"+str(randomWord(len(Seed))))
        print("srw:"+str(SrandomWord(len(Seed))))
        print("scw:"+scatterWord(Seed))
