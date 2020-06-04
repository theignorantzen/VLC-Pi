lp = T = 5000 # no of bits, length of input
 
master = "01100101"
inp = ""
# read the data
while lp:
	t = input()
	inp += str(t)
	lp -= 1
 
start = 0
end = T
inp = inp[start: end]
k = len(inp)
l = len(master)
# code for accuracy
accu = [0]*l
for i in xrange(l):
	inp_ = inp[i:]
	for j in xrange(len(inp_)):
		if master[j%l] == inp_[j%k]:
			accu[i] += 1
 
print "accuracy:", accu
print "accuracy in %:", [100*(accu[i])/(k-i) for i in range(len(accu))]
