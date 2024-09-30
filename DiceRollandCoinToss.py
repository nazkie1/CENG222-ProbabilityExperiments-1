import numpy as np
import random
from matplotlib import pyplot as plt

# Experiment 1 -- 6 & 4 sided dice roll alongside a coin toss

ar_A = []
ar_B = []
ar_C = []
ar_X = []

av_A = []
av_B = []
av_C = []
av_X = []
vr_X = []

# Populate the given arrays.

A_total = 0
B_total = 0
C_total = 0
X_total = 0

avg_A = 0
avg_B = 0
avg_C = 0
avg_X = 0

for i in range(30000):
    ##### A
    a = 6 * random.random() #expanded the interval to 0 - 6

    if a < 1:
        a = 1
    elif  1 < a < 2:
        a = 2
    elif 2 < a < 3:
        a = 3
    elif 3 < a < 4:
        a = 4
    elif 4 < a < 5:
        a = 5
    elif 5 < a < 6:
        a = 6
    ar_A.append(a)    #filled ar_A, got avg values and filled av_A
    A_total += ar_A[i]
    avg_A = A_total / (i+1)
    av_A.append(avg_A)

    ###### B
    b = 4 * random.random() #expanded the interval to 0-4

    if b < 1:
        b = 1
    elif 1 < b < 2:
        b = 2
    elif 2 < b < 3:
        b = 3
    elif 3 < b < 4:
        b = 4
    ar_B.append(b)     #filled ar_B, got avg values and filled av_B
    B_total += ar_B[i]
    avg_B = B_total / (i+1)
    av_B.append(avg_B)

    ###### C
    c = random.random()
    if c < (0.5):
        c = +1
    elif (0.5) < c < 1:
        c = -1
    ar_C.append(c)  #filled ar_C, got avg values and filled av_C
    C_total += ar_C[i]
    avg_C= C_total / (i+1)
    av_C.append(avg_C)

    ###### X
    x = a + ( b * c )
    ar_X.append(x) #filled ar_X, got avg values and filled av_X
    X_total += ar_X[i]
    avg_X = X_total / (i+1)
    av_X.append(avg_X)


#used the formula var(X) = (sum of((xi - e(x))^2) from 1 to n ) / (n - 1) and filled vr_X
diff_squared = 0
var_X = 0
for j in range(1, len(ar_X)+1):

    diff_squared += (ar_X[j-1] - av_X[j-1]) ** 2
    var_X = diff_squared / j
    vr_X.append(var_X)



# Inspect the following plots. 

plt.figure()
plt.hist(ar_A,6,range=(1,7),align='left',density=True, rwidth=0.8)
plt.figure()
plt.hist(ar_B,4,range=(1,5),align='left',density=True, rwidth=0.8)
plt.figure()
plt.hist(ar_C,3,range=(-1,2),align='left',density=True, rwidth=0.8)
plt.figure()
plt.hist(ar_X,14,range=(-3,11),align='left',density=True, rwidth=0.8)

# Plot the average and variance values.
### YOUR CODE HERE ###

x_values = range(30000)

# Plot "Average of A" (figure 5)
plt.figure()
plt.plot(x_values, av_A, label='Average A')
plt.title('Average of A')
plt.legend()
plt.grid()


# Plot "Average of B" (figure 6)
plt.figure()
plt.plot(x_values, av_B, label='Average B')
plt.title('Average of B')
plt.legend()
plt.grid()


# Plot "Average of C" (figure 7)
plt.figure()
plt.plot(x_values, av_C, label='Average C')
plt.title('Average of C')
plt.legend()
plt.grid()


# Plot "Average of X" (figure 8)
plt.figure()
plt.plot(x_values, av_X, label='Average X')
plt.title('Average of X')
plt.legend()
plt.grid()


# Plot "Variance of X" (figure 9)
plt.figure()
plt.plot(x_values, vr_X, label='Variance of X')
plt.title('Variance of X')
plt.legend()
plt.grid()


# Experiment 2

# Part a (Inverse Transform Method)
U = []
Xa = []
av_Xa = []
vr_Xa = []

# Populate the given arrays.
### YOUR CODE HERE ###

#used x^2 = u ---> x = √u and generated Xa values
for i in range(30000):
    u = random.random()
    xa = u ** (0.5)
    U.append(u)
    Xa.append(xa)

Xa_total = 0
avg_Xa = 0

#calculated "Average of Xa" and filled av_Xa
for i in range(30000):
    Xa_total += Xa[i]
    avg_Xa = Xa_total / (i+1)
    av_Xa.append(avg_Xa)

#used the formula var(X) = (sum of((xi - e(x))^2) from 1 to n ) / (n - 1) and filled vr_Xa
diff_squared_2 = 0
var_Xa = 0
for j in range(1, len(Xa)+1):

    diff_squared_2 += (Xa[j-1] - av_Xa[j-1]) ** 2
    var_Xa = diff_squared_2 / j
    vr_Xa.append(var_Xa)
    
# Inspect the following plots.
plt.figure()
for i in range(len(Xa)):
    plt.plot([Xa[i],U[i]],[1,1.2])
plt.figure()
hU = plt.hist(U,100,alpha=0.5,density=True)
hXa = plt.hist(Xa,100,alpha=0.5,density=True)
plt.figure()
plt.plot(np.cumsum(hU[0]))
plt.plot(np.cumsum(hXa[0]))

#Plot the average and variance values.
x_values = range(30000)

# Plot "Average of Xa" (figure 13)
plt.figure()
plt.plot(x_values, av_Xa, label = 'Average Xa')
plt.title('Average of Xa')
plt.legend()
plt.grid()

# Plot "Variance of Xa" (figure 14)
plt.figure()
plt.plot(x_values, vr_Xa, label = 'Variance Xa')
plt.title('Variance of Xa')
plt.legend()
plt.grid()



# Part b (Rejection Method)
Xb = []
av_Xb = []
vr_Xb = []


# Populate the given arrays.
### YOUR CODE HERE ###

#defined function g(x) = F'(x) = 2x
def g(x):
    return 2*x

# a-b x interval and c is max y value
a = 0
b = 1
c = g(b)

#created (xb, y) values with random u and v
u = random.random()
v = random.random()
xb = a + (b - a) * u
Y = c * v

#if y <= g(xb), we accepted the points and put those xb in Xb
for i in range (30000): 
    u = random.random()
    v = random.random()
    xb = a + (b - a) * u
    Y = c * v
    if Y <= g(xb):
        Xb.append(xb)

Xb_total = 0
avg_Xb = 0

#calculated "Average of Xb" and filled av_Xb
for k in range(len(Xb)):
    Xb_total += Xb[k]
    avg_Xb = Xb_total / (k+1)
    av_Xb.append(avg_Xb)  


#used the formula var(X) = (sum of((xi - e(x))^2) from 1 to n ) / (n - 1) and filled vr_Xb
diff_squared_2b = 0
var_Xb = 0
for j in range(1, len(Xb)+1):

    diff_squared_2b += (Xb[j-1] - av_Xb[j-1]) ** 2
    var_Xb = diff_squared_2b / j
    vr_Xb.append(var_Xb)

        
# Inspect the following plots.
plt.figure()    
hXb = plt.hist(Xb,100,density=True)
plt.figure()
plt.plot(np.cumsum(hXb[0]))

# Plot the average and variance values.
### YOUR CODE HERE ###

x_values_2b = range(len(Xb))
# Plot "Average of Xb" (figure 17)
plt.figure()
plt.plot(x_values_2b, av_Xb, label='Average of Xb')
plt.title('Average of Xb')
plt.legend()
plt.grid()


# Plot "Variance of Xb" (figure 18)
plt.figure()
plt.plot(x_values_2b, vr_Xb, label='Variance of Xb')
plt.title('Variance of Xb')
plt.legend()
plt.grid()
plt.show()
