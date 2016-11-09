'''
Created on Jul 20, 2016
@author: Niveditha
'''
import math
import re
import sys
import os

class ProbG:
    prob = []
    g = 0.0
    direction = 'F'
    ind = 0

'''
Function name: calculate_error
Description: calculates threshold with minimum error
'''
def calculate_prob_g(y, p, n):
    min_g = sys.float_info.max
    direc = 'N'
    obj1 = ProbG()
    for i in range(1, n):
        pr_plus = 0.0
        pr_minus = 0.0
        pw_plus = 0.0
        pw_minus = 0.0
        for j in range(0, n):
            if (j < i):
                if (y[j] == -1):
                    pw_minus = pw_minus + p[j]
                else:
                    pr_plus = pr_plus + p[j]

            else:
                if (y[j] == -1):
                    pr_minus = pr_minus + p[j]
                else:
                    pw_plus = pw_plus + p[j]

        g = math.sqrt(pr_plus * pw_minus) + math.sqrt(pw_plus * pr_minus)
        direc = 'F'
        if (g > 0.5):
            g = 1 - g
            temp = pr_plus
            pr_plus = pw_plus
            pw_plus = temp
            temp = pr_minus
            pr_minus = pw_minus
            pw_minus = temp
            direc = 'R'

        if (g < min_g):
            obj1.prob = []
            min_g = g
            obj1.g = g
            obj1.direction = direc
            obj1.ind = i
            obj1.prob.append(pr_plus)
            obj1.prob.append(pr_minus)
            obj1.prob.append(pw_plus)
            obj1.prob.append(pw_minus)

    return obj1

'''
Function name: iteration
Description: calculates all the values needed for one iteration
'''
def iteration(n,epsilon,p,x,y):
    global ftemp
    global e_t
    obj_prob_g = calculate_prob_g(y,p,n)
    weak_class = 0.0
    if (obj_prob_g.ind == 0):
        weak_class = (x[obj_prob_g.ind]- 1)
    else:
        weak_class = (x[obj_prob_g.ind] + x[obj_prob_g.ind - 1]) /2

    if (obj_prob_g.direction == 'F'):
        print("The selected weak classifier Ht: I( x < ", weak_class,  ") ")
    elif(obj_prob_g.direction == 'R'):
        print("The selected weak classifier Ht: I( x > ", weak_class, ") ")

    print("The G error value of Ht: ", obj_prob_g.g)
    c_t_plus = (1.0 / 2.0) * math.log(float((obj_prob_g.prob[0] + epsilon) / (obj_prob_g.prob[3] + epsilon)))
    c_t_minus = (1.0 / 2.0) * math.log((obj_prob_g.prob[2] + epsilon) / (obj_prob_g.prob[1] + epsilon))
    print("The weights Ct+, Ct-: ", c_t_plus, ", ",c_t_minus)

    sum = 0.0
    for i in range(0, n):
        if (i < obj_prob_g.ind):
            p[i] = p[i] * math.pow(math.e, (-1) * c_t_plus * y[i])
        else:
            p[i] = p[i] * math.pow(math.e, (-1) * c_t_minus * y[i])
        sum = sum +p[i]

    print("The probabilities normalization factor Zt: ", sum)
    print("The probabilities after normalization: ")
    for i in range(0, n):
        p[i] = p[i] /sum
        if (i == 0):
            print(p[i], end='')
        else:
            print(", ", p[i], end='')
    print()
    errors = 0.0
    print("The values ft(xi) for each one of the examples: ")
    for i in range(0, n):
        if (x[i] < weak_class):
            ftemp[i] = ftemp[i] + c_t_plus

        else:
            ftemp[i] = ftemp[i] + c_t_minus
        if (i == 0):
            print(ftemp[i],end='')
        else:
            print(", ",ftemp[i], end='')

        if ((y[i] > 0 and ftemp[i] < 0) or (y[i] < 0 and ftemp[i] >= 0)):
            errors = errors + 1
    print()
    print("The error of the boosted classifier Et: ", errors /float(n))
    e_t = e_t * sum
    print("The bound on Et: ", e_t)
    return p

x = []
y = []
p = []
ftemp = []
e_t = 1
T_n_epsilon = []
filename = "input.txt"
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
            print("Iteration ", (j + 1), ":")
            p =  iteration(int(T_n_epsilon[1]),float(T_n_epsilon[2]), p, x, y)
            print(" ")

    except IOError:
        print("Could not read file:", filename)
        exit(0)

else:
    print("The input file name given does not exist. Please try again with correct input file name")
    exit(0)


