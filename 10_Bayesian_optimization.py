##  https://scikit-optimize.github.io/notebooks/bayesian-optimization.html
import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize
##  Implemented in /home/sbn/anaconda2/lib/python2.7/site-packages/skopt/optimizer/base.py
##  Implemented in /home/sbn/anaconda2/lib/python2.7/site-packages/skopt/optimizer/optimizer.py
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from skopt.space import Integer

from helper_function_2 import *
import codecs, json
import subprocess 
#%matplotlib inline
from skopt.plots import plot_convergence
import time

probed_points_x=[]
probed_points_y=[]
#################################################################
def allocation(allocation_vector):
    sum=0
    # Need to get the response time value from the controller
    writeAllocMatToFile(allocation_vector)
    subprocess.call(['./run_client_for_execution.sh'])
    var_aa_22=STATUS_MONITOR_MODULE_PATH+"run_results/resp_time/resp_run/avg_resp_run.csv"
    sum=getDictFrom(var_aa_22)
    #for i in range(0,max_no_of_micro_services):
    #    sum+=np.sin(allocation_vector[i])
    #print("Allocation(",allocation_vector,")=",sum)
    global probed_points_x
    global probed_points_y
    probed_points_x.append(allocation_vector)
    probed_points_y.append(sum)
    return sum
#################################################################
def writeToFile(A):
    putDictTo('final_alloc_matrix_output.txt',A)
    node_final=np.zeros((no_of_services,max_no_of_micro_services,index_of_fog_node,no_of_time_slots))
    node_final4=np.chararray(node_final.shape, itemsize=15)

    for i in range(0,no_of_services):
        for j in range(0,max_no_of_micro_services):
            for l in range(0,no_of_time_slots):
                node_final4[i][j][0][l]=map_fog_ip(A[i][j][0][l])

    #json.dump(node_final4.tolist(), codecs.open('final_alloc_matrix_output_3.txt', 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    putDictTo('final_alloc_matrix_output_3.txt',node_final4.tolist())
#################################################################
def writeAllocMatToFile(x_min):
    # Convert row major to 2 dimension matrix
    arr=rowMajorTo2D(x_min,**params)
    A=arr.tolist()
    # Write the allocation matrix to a file
    writeToFile(A)
#################################################################
params={"no_of_fog_nodes":no_of_fog_nodes,"no_of_resource_type":no_of_resource_type,"no_of_time_slots":no_of_time_slots,"total_quantity_of_resource_needed":total_quantity_of_resource_needed,"no_of_services":no_of_services,"max_no_of_micro_services":max_no_of_micro_services,"index_of_fog_node":index_of_fog_node}
space = [Integer(0,no_of_fog_nodes) for i in range(max_no_of_micro_services)]
actualSpace=ConstrainedSpace(space,constraint=IsFeasible,**params)

X=[]
X1=getDictFrom('ini_alloc_mat_1.txt')
X2=getDictFrom('ini_alloc_mat_2.txt')
X.append(X1)
X.append(X2)

Y=[]
start_time = time.time()
Y1=allocation(X[0])
Y.append(Y1)
print "Y1 is:",Y1
itr_cnt=1
time_taken0 = time.time() - start_time
start_time = time.time()
Y2=allocation(X[1])
Y.append(Y2)
print "Y2 is:",Y2
time_taken1 = time.time() - start_time
print "#####################" 
print "Iteration number:",itr_cnt
print "#####################"

if(Y1<Y2):
    print "Min value of function till this iteration:", Y1
    print "Corresponding allocation matrix is:",X[0]
    print "Time taken to perform this iteration is ", time_taken0, "seconds."
else:
    print "Min value of function till this iteration:", Y2
    print "Corresponding allocation matrix is:",X[1]
    print "Time taken to perform this iteration is ", time_taken1, "seconds."

print "End of iteration number:",itr_cnt
print "#####################"

for i in xrange(1,400):
    start_time = time.time()
    res = gp_minimize(allocation,          # the function to minimize
        actualSpace,                       # space i.e. the bounds on each dimension of x
        base_estimator=None,               # kernel function
        acq_func="EI",                     # the acquisition function
        n_random_starts=0,                 # reduce number of evaluation of target function
        x0=X,                              # initial training data
        y0=Y,
        verbose=False,
        n_calls=1)                         # the number of evaluations of function allocation 
    plot_convergence(res)
    print "Loop counter is:",i
    if(len(probed_points_x) > 0):
        x_i=probed_points_x[-1]
        y_i=probed_points_y[-1]
        #y_i=allocation(x_i)
        X.append(x_i)
        Y.append(y_i)
        
    if(res.func_vals[i+1]!=999):
        itr_cnt+=1
        print "#####################"
        print "Iteration number:",itr_cnt
        print "#####################"
        print "Value of function returned in this step:",res.func_vals[i+1]
        print "Corresponding allocation matrix returned in this step is:",res.x_iters[i+1]
        #print "All value of function returned:",res.func_vals
        #print "All allocation matrix returned is:",res.x_iters
        time_taken = time.time() - start_time
        print "Time taken to perform this iteration is ", time_taken, "seconds."
        print "Min value of function till this iteration:", np.min(res.func_vals)
        print "End of iteration number:",itr_cnt
        print "#####################"

#print "FINAL OUTPUT\n X=",X,"\n\nY=",Y
index_x_min=np.argmin(Y)
x_min=X[index_x_min]
print "x_min is:",x_min 
print "y_min is:",Y[index_x_min]
writeAllocMatToFile(x_min)
#################################################################
def plot_function():
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x=[ i for i in xrange(0,90)]
    y=[ i for i in xrange(0,90)]
    z=[]
#################################################################
