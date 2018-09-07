from guppy import hpy
def cache(func):
    cached = {}
    def _func(args):
        if args not in cached:
            cached[args] = func(args)
        return cached[args]
    
    return _func

@profile
def fab(n):
    #hp = hpy()
    #print "Heap at the beginning of the functionn", hp.heap()
    if n==0 or n==1:
        return n
    else:
        return fab(n-1) + fab(n-2)
    #print "Heap at the end of the functionn", hp.heap()

#print fab(0), fab(1), fab(2), fab(3), fab(4), fab(5)
print fab(35)

