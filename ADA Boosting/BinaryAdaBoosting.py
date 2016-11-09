'''
Created on Jul 20, 2016
@author: Niveditha
'''
import math
import re
import os


'''
Function name: calculate_error
Description: calculates threshold with minimum error
'''
def calculate_error(y,n,p):
    e = []
    error = 0.0
    index = 0
    min_error = 1.0
    direction = 'F'
    for i in range(0, n):
        if (y[i] == 1):
            error = p[i] + error
    if (error > 0.5):
        temp_error= 1-error
        if (temp_error < min_error):
            min_error = temp_error
            direction = 'R'
    else:
        if (error < min_error):
            min_error = error
            direction = 'F'
    for i in range(0, n):
        if (y[i] == -1):
            error = error + p[i]
        else:
            error = error - p[i]
        if (error > 0.5):
            temp_error= 1-error
            if (temp_error < min_error):
                min_error = temp_error
                direction = 'R'
                index = i
        else:
            if (error < min_error):
                min_error = error
                direction = 'F'
                index = i
    e.append(index)
    e.append(min_error)
    e.append(direction)
    return e

'''
Function name: iteration
Description: calculates all the values needed for one iteration
'''
def iteration(n,p,x,y):
    global boosted_classifier
    global ftemp
    global e_t
    min_error = calculate_error(y,n,p)
    weak_class = 0.0
    if (min_error[0] == (n - 1)):
        weak_class = (x[min_error[0]]+ 1)
    else:
        weak_class = ((x[min_error[0]] + x[min_error[0] + 1]) / 2)
    if(min_error[2] == 'F'):
        print("The selected weak classifier Ht: x <", weak_class)
    elif (min_error[2] == 'R'):
        print("The selected weak classifier Ht: x >", weak_class)
    print("The error of Ht: ", min_error[1])
    alpha = (1 / 2)*math.log((1 - min_error[1]) / min_error[1])

    print("The weight of Ht: ", alpha)
    sum_pq = 0.0
    h = 0
    if (min_error[2] == 'F'):
        h = 1
    else:
        h = -1

    for i in range(0, n):
        if (i <= min_error[0]):
            p[i]= p[i] * (math.pow(math.e, (-1) * alpha * y[i] * h))

        else:
            p[i]= p[i] * (math.pow(math.e, alpha * y[i] * h))

        sum_pq= sum_pq+p[i]
    print("The probabilities normalization factor Zt: ", sum_pq)
    print("The probabilities after normalization: ",end='')
    for i in range(0, n):
        p[i] = (p[i] /sum_pq)
        if(i==0):
            print(p[i], end='')
        else:
            print( ", ",p[i], end='')
    print(" ")
    if (min_error[2] == 'F'):
        boosted_classifier = ''.join([boosted_classifier, str(alpha) , " * " , "I (x < " , str(weak_class), ") + "])
    elif (min_error[2] == 'R'):
        boosted_classifier = ''.join([boosted_classifier, str(alpha), " * ", "I (x > ", str(weak_class), ") + "])
    print("The boosted classifier: ", boosted_classifier[:-2])
    errors = 0.0
    for i in range(0, n):
        if (min_error[2] == 'F'):
            if (x[i] < weak_class):
                ftemp[i]= ftemp[i] + (alpha * 1)
            else:
                ftemp[i]= ftemp[i] + (alpha * -1)

        else:
            if (x[i] > weak_class):
                ftemp[i]= ftemp[i] + (alpha * 1)
            else:
                ftemp[i]= ftemp[i] + (alpha * -1)
        if ((y[i] > 0 and ftemp[i] < 0) or (y[i] < 0 and ftemp[i] >= 0)):
            errors = errors + 1

    print("The error of the boosted classifier: ", errors/float(n))
    e_t = e_t * sum_pq
    print("The bound on Et: ", e_t)
    return p

boosted_classifier = ''
ftemp = []
e_t = 1
x = []
y = []
p = []
T_n_epsilon = []
filename = "adaboost-2.txt"
if os.path.exists(filename):
    try:
        fileobj1 = open(filename, 'r')
        header = fileobj1.readline().strip('\n')
        T_n_epsilon.extend(re.split('\s+', header))
        T_n_epsilon = [float(i) for i in T_n_epsilon]
        line = fileobj1.readline().strip('\n')
        x.extend(re.split('\s+', line))
        x = [float(i) for i in x]
        line = fileobj1.readline().strip('\n')
        y.extend(re.split('\s+', line))
        y = [int(i) for i in y]
        line = fileobj1.readline().strip('\n')
        p.extend(re.split('\s+', line))
        p = [float(i) for i in p]
        fileobj1.close()
        for i in range(0, int(T_n_epsilon[1])):
            ftemp.append(0)
        for j in range(0, int(T_n_epsilon[0])):
            print("Iteration", (j + 1))
            p =  iteration(int(T_n_epsilon[1]), p, x, y)
            print(" ")
    except IOError:
        print("Could not read file:", filename)
        exit(0)

else:
    print("The input file name given does not exist. Please try again with correct input file name")
    exit(0)