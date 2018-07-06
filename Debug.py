from time import gmtime, strftime

#Logname = "Debug-{}".format(strftime("Debug-%H:%M:%S", gmtime()))
Logname = strftime("Debug-%H.%M.%S.log", gmtime())

def Log(s):
    open(Logname,'w').write(s)
