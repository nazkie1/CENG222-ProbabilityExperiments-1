# %% Imports
import random
import numpy as np
from matplotlib import pyplot as plt


# %% Functions

# Function to generate a population with given parameter and size using the
# inverse transformation method.

def gen_inverse(k, M):
    X = np.zeros(M)

    # u random var for x creation
    for i in range (M):
        u = random.random()
        x = u ** (1/(k+1))
        X[i] = x

    return X
      
# Function to generate a population with given parameter and size using the
# rejection method.

def gen_rejection(k, M):
    def f(x):
        return (k+1) * (x**k)
    
    X = np.zeros(M)
    a = 0
    b = 1
    c = f(b)

    # v and t random var for x y creation
    i = 0
    while i < M:
        v = random.random()
        t = random.random()
        x = a + (b - a)* v
        y = c * t

        if y <= f(x):
            X[i] = x
            i +=1
    return X

# Function to calculate the population mean using k.
def calc_population_mean(k):

    def E(x):
        return (k + 1) * (x ** (k+2)) / (k+2)
    mean = E(1) - E(0)
    return mean

# Function to calculate the population variance using k.

# var = E(x^2) - E(x)^2. E(x^2) = (k+1) / (k+3) for [0,1] interval.
def calc_population_variance(k):
    return ((k+1) / (k+3)) - (calc_population_mean(k)**2)

# Function to randomly take samples of size N from a population.
def random_sample(population, N):
     return np.random.choice(population, N)

# Function to calculate the sample mean.
def calc_sample_mean(sample):
    return np.sum(sample) / (len(sample))


# Function to calculate the sample variance (biased/unbiased).
def calc_sample_variance(sample, unbiased=True):
    diff_squared = 0
    sample_mean = calc_sample_mean(sample)
    for i in range (len(sample)):
        diff_squared += (sample[i] - sample_mean) ** 2
    if unbiased:
        sample_variance = diff_squared / (len(sample) - 1)
    else:
        sample_variance = diff_squared / len(sample)
    return sample_variance

# Function to estimate the parameter k using method of moments

#Use population mean = sample mean, we found population mean (k + 1)/(k + 2) above. And calculated sample mean via 6th function.
def estimate_k_mom(sample):
    sample_mean = calc_sample_mean(sample)

    #sample mean = (k + 1)/(k + 2). Solve for k. 
    estimated_k = (2 * sample_mean - 1)/ (1 - sample_mean)

    return estimated_k

# Function to estimate the parameter k using maximum likelihood
def estimate_k_mle(sample):
    #our pdf for x is (k + 1) * x^k. 
    # 1- take ln of pdf and sum all [i=1, sample size]
    # 2- take partial derivative of 1 with respect to k. 
    # 3- Equation 2 = 0
    # 4- Solve 3 for k. estimated k = - (sample size / sum all(lnX)) - 1
    
    sample_size = len(sample)
    log_of_xi = np.log(sample)
    sum_of_all_logs = np.sum(log_of_xi)

    estimated_k =  ((- sample_size / sum_of_all_logs) - 1)

    return estimated_k

# Function to calculate the confidence interval for population mean given the
# sample and the required confidence level. If population standard deviation is
# not provided, use sample standard deviation as its estimator. As confidence
# level, it should only accept 95, 96, 97, 98 and 99 for which the z values are
# hard-coded in the function.
def calc_conf_int_mean(sample, confidence_lvl, pop_std=0):

    if confidence_lvl == 95:
        z = 1.96
    elif confidence_lvl == 96:
        z = 2.05
    elif confidence_lvl == 97:
        z = 2.17
    elif confidence_lvl == 98:
        z = 2.33
    elif confidence_lvl == 99:
        z = 2.57
    else:
        raise ValueError("Invalid confidence level")
    
    if pop_std == 0:
        sample_std_deviation = (calc_sample_variance(sample, unbiased=True)) ** (1/2)     
    else:
        sample_std_deviation = pop_std

    sample_mean = calc_sample_mean(sample)
    interval = [(sample_mean - z * (sample_std_deviation/((len(sample))**(1/2)))), (sample_mean + z * (sample_std_deviation/((len(sample))**(1/2))))]
    return interval


# %% Experiments

# Generate the two populations of size 1000000, calculate and print their means
# and variances and plot the population histograms.
M = 1000000
k_1 = 2.1
k_2 = 3.7
conf_lvl = 97

# YOUR CODE HERE

population_1 = gen_inverse(k_1, M)
mean_1 = calc_population_mean(k_1)
variance_1 = calc_population_variance(k_1)

population_2 = gen_rejection(k_2, M)
mean_2 = calc_population_mean(k_2)
variance_2 = calc_population_variance(k_2)

print("Population 1:")
print(f"Mean: {mean_1} \nVariance: {variance_1}")

print()

print("Population 2:")
print(f"Mean: {mean_2} \nVariance: {variance_2}")

plt.figure()
plt.hist(population_1, bins=50, alpha=0.5, label='Population 1')
plt.hist(population_2, bins=50, alpha=0.5, label='Population 2')
plt.legend()
plt.title('Population Histograms')
plt.show()

# YOUR CODE HERE

# Collect 100000 random samples of size 25 from both populations, calculate
# sample means, biased and unbiased sample variances, MoM and MLE estimates of
# the parameter k and population mean intervals with 97% confidence with and
# without the population standard deviation for each sample of each population.
N = 25
R = 100000

# YOUR CODE HERE

s1_means = []
s2_means = []

s1_biased_vars  = []
s1_unbiased_vars  = []
s2_biased_vars  = []
s2_unbiased_vars = []

s1_MoM_est = []
s1_MLE_est = []
s2_MoM_est = []
s2_MLE_est = []

s1_conf_int_w_popstd = []
s1_conf_int_wo_popstd = []
s2_conf_int_w_popstd = []
s2_conf_int_wo_popstd = []

population1_std = variance_1 ** (1/2)
population2_std = variance_2 ** (1/2)
for i in range (R):
    #sample_1.append(random_sample(population_1, N))
    sample_1 = random_sample(population_1, N)
    sample_2 = random_sample(population_2, N)

    means_of_s1 = calc_sample_mean(sample_1)
    s1_means.append(means_of_s1)
    means_of_s2 = calc_sample_mean(sample_2)
    s2_means.append(means_of_s2)

    biased_vars_of_s1 = calc_sample_variance(sample_1, unbiased=False)
    s1_biased_vars.append(biased_vars_of_s1)
    unbiased_vars_of_s1 = calc_sample_variance(sample_1, unbiased=True)
    s1_unbiased_vars.append(unbiased_vars_of_s1)
    biased_vars_of_s2 = calc_sample_variance(sample_2, unbiased=False)
    s2_biased_vars.append(biased_vars_of_s2)
    unbiased_vars_of_s2 = calc_sample_variance(sample_2, unbiased=True)
    s2_unbiased_vars.append(unbiased_vars_of_s2)

    s1_MoMs = estimate_k_mom(sample_1)
    s1_MoM_est.append(s1_MoMs)
    s1_MLEs = estimate_k_mle(sample_1)
    s1_MLE_est.append(s1_MLEs)

    s2_MoMs = estimate_k_mom(sample_2)
    s2_MoM_est.append(s2_MoMs)
    s2_MLEs = estimate_k_mle(sample_2)
    s2_MLE_est.append(s2_MLEs)

    s1_intervals_w_std = calc_conf_int_mean(sample_1, 97, population1_std)
    s1_conf_int_w_popstd.append(s1_intervals_w_std)
    s1_intervals_wo_std = calc_conf_int_mean(sample_1, 97)
    s1_conf_int_wo_popstd.append(s1_intervals_wo_std)

    s2_intervals_w_std = calc_conf_int_mean(sample_2, 97, population2_std)
    s2_conf_int_w_popstd.append(s2_intervals_w_std)
    s2_intervals_wo_std = calc_conf_int_mean(sample_2, 97)
    s2_conf_int_wo_popstd.append(s2_intervals_wo_std)


# Calculate and print means of sample means, biased and unbiased sample
# variances, MoM and MLE estimates of parameter k and plot the histograms of
# sample means, k estimates using MoM and MLE for both populations.

# YOUR CODE HERE
mean_of_means1 = np.sum(s1_means) / R
mean_of_biased_vars1 = np.sum(s1_biased_vars) / R
mean_of_unbiased_vars1 = np.sum(s1_unbiased_vars) / R
mean_of_MoM_est1 = np.sum(s1_MoM_est) / R
mean_of_MLE_est1 = np.sum(s1_MLE_est) / R

print()
print("For SAMPLE 1:")
print(f"Mean of means: {mean_of_means1}")
print(f"Mean of biased variances: {mean_of_biased_vars1}")
print(f"Mean of unbiased variances: {mean_of_unbiased_vars1}")
print(f"Mean of MoM estimates: {mean_of_MoM_est1}")
print(f"Mean of MLE estimates: {mean_of_MLE_est1}")

mean_of_means2 = np.sum(s2_means) / R
mean_of_biased_vars2 = np.sum(s2_biased_vars) / R
mean_of_unbiased_vars2 = np.sum(s2_unbiased_vars) / R
mean_of_MoM_est2 = np.sum(s2_MoM_est) / R
mean_of_MLE_est2 = np.sum(s2_MLE_est) / R

print()
print("For SAMPLE 2:")
print(f"Mean of means: {mean_of_means2}")
print(f"Mean of biased variances: {mean_of_biased_vars2}")
print(f"Mean of unbiased variances: {mean_of_unbiased_vars2}")
print(f"Mean of MoM estimates: {mean_of_MoM_est2}")
print(f"Mean of MLE estimates: {mean_of_MLE_est2}")
plt.figure()
# YOUR CODE HERE

plt.hist(s1_means, bins=50, alpha=0.5, label='Sample means - Population 1')
plt.hist(s2_means, bins=50, alpha=0.5, label='Sample means - Population 2')
plt.legend()
plt.title('Histogram of Sample Means')
plt.show()


plt.figure()
# YOUR CODE HERE

plt.hist(s1_MoM_est, bins=50, alpha=0.5, label='MoM estimates - Population 1')
plt.hist(s2_MoM_est, bins=50, alpha=0.5, label='MoM estimates - Population 2')
plt.legend()
plt.title('Histogram of MoM Estimates')
plt.show()

plt.figure()
# YOUR CODE HERE

plt.hist(s1_MLE_est, bins=50, alpha=0.5, label='MLE estimates - Population 1')
plt.hist(s2_MLE_est, bins=50, alpha=0.5, label='MLE estimates - Population 2')
plt.legend()
plt.title('Histogram of MLE Estimates')
plt.show()

# Calculate and print the ratio of confidence intervals computed with and
# without using the population standard deviation that contains the population
# mean for both populations.

# YOUR CODE HERE

def conf_int_include_pop_mean(conf_interval, population_mean):
    return conf_interval[0] <= population_mean <= conf_interval[1]

#Population 1 için
pop_1_ci_w_std_count = 0
pop_1_ci_wo_std_count = 0

for i in (s1_conf_int_w_popstd):
    if conf_int_include_pop_mean(i, mean_1):
        pop_1_ci_w_std_count +=1
pop_1_ci_w_std_ratio = pop_1_ci_w_std_count / R

for i in (s1_conf_int_wo_popstd):
    if conf_int_include_pop_mean(i, mean_1):
        pop_1_ci_wo_std_count +=1
pop_1_ci_wo_std_ratio = pop_1_ci_wo_std_count / R

pop_2_ci_w_std_count = 0
pop_2_ci_wo_std_count = 0

for i in (s2_conf_int_w_popstd):
    if conf_int_include_pop_mean(i, mean_2):
        pop_2_ci_w_std_count +=1
pop_2_ci_w_std_ratio = pop_2_ci_w_std_count / R

for i in (s2_conf_int_wo_popstd):
    if conf_int_include_pop_mean(i, mean_2):
        pop_2_ci_wo_std_count +=1
pop_2_ci_wo_std_ratio = pop_1_ci_wo_std_count / R
print()
print("Confidence intervals for population 1:")
print(f"Ratio of confidence intervals with std: {pop_1_ci_w_std_ratio}")
print(f"Ratio of confidence intervals without std: {pop_1_ci_wo_std_ratio}")
print("Confidence intervals for population 2:")
print(f"Ratio of confidence intervals with std: {pop_2_ci_w_std_ratio}")
print(f"Ratio of confidence intervals without std: {pop_1_ci_wo_std_ratio}")

print('*'*50)
# Collect a sample of length 100000*25 from both populations, calculate and
# print their sample means, biased and unbiased sample variances, MoM and MLE
# estimates of parameter k and confidence intervals with and without using the
# population standard deviation.

# YOUR CODE HERE
big_sample_1 =random_sample(population_1, 2500000)
big_sample_1_mean = calc_sample_mean(big_sample_1)
biased_big_sample_1_var = calc_sample_variance(big_sample_1, unbiased=False)
unbiased_big_sample_1_var = calc_sample_variance(big_sample_1, unbiased=True)
big_sample_1_MoM_est = estimate_k_mom(big_sample_1)
big_sample_1_MLE_est = estimate_k_mle(big_sample_1)
big_sample_1_conf_int_w_popstd = calc_conf_int_mean(big_sample_1, 97, population1_std)
big_sample_1_conf_int_wo_popstd = calc_conf_int_mean(big_sample_1, 97)

big_sample_2 = random_sample(population_2, 2500000)
big_sample_2_mean = calc_sample_mean(big_sample_2)
biased_big_sample_2_var = calc_sample_variance(big_sample_2, unbiased=False)
unbiased_big_sample_2_var = calc_sample_variance(big_sample_2, unbiased=True)
big_sample_2_MoM_est = estimate_k_mom(big_sample_2)
big_sample_2_MLE_est = estimate_k_mle(big_sample_2)
big_sample_2_conf_int_w_popstd = calc_conf_int_mean(big_sample_2, 97, population2_std)
big_sample_2_conf_int_wo_popstd = calc_conf_int_mean(big_sample_2, 97)

print("For Big Sample from Population 1:")
print()
print(f"Sample Mean: {big_sample_1_mean}")
print(f"Biased Variance: {biased_big_sample_1_var}")
print(f"Uniased Variance: {unbiased_big_sample_1_var}")
print(f"MoM Estimation: {big_sample_1_MoM_est}")
print(f"MLE Estimation: {big_sample_1_MLE_est}")
print(f"Confidence Interval with population std: {big_sample_1_conf_int_w_popstd}")
print(f"Confidence Interval without population std: {big_sample_1_conf_int_wo_popstd}")

print()

print("For Big Sample from Population 2:")
print()
print(f"Sample Mean: {big_sample_2_mean}")
print(f"Biased Variance: {biased_big_sample_2_var}")
print(f"Uniased Variance: {unbiased_big_sample_2_var}")
print(f"MoM Estimation: {big_sample_2_MoM_est}")
print(f"MLE Estimation: {big_sample_2_MLE_est}")
print(f"Confidence Interval with population std: {big_sample_2_conf_int_w_popstd}")
print(f"Confidence Interval without population std: {big_sample_2_conf_int_wo_popstd}")