#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Import the required libraries
import random
import numpy as np
import matplotlib.pyplot as plt


# 1.a Code up their model (in any language of choice) and 
# recreate one of the curves in Figure 1.You don’t need to have as many points as them, 
# but the trend / line should be visible. 

# In[2]:


# Define list to store evolutionarily stable switching rates
evolutionarily_stable_switching_rates = []

# Define mean waiting time
mean_waiting_time = 20

# Define selection coefficients
s = s_0 = s_1 = 0.1

# Initialize figure
fig, ax = plt.subplots()

# Define the range of variances of waiting times
variances = np.linspace(0, 400, 20)

# Step 1: Initialize the population with random allele frequencies
major_allele_freq = random.uniform(0, 1)
modifier_allele_freq = 1

# Step 2: Choose the initial environment randomly
if random.random() < 0.5:
    environment = "e0"
else:
    environment = "e1"

# Step 3: Define mutation rates
mM = 0.01
mm = 0.1

# Step 4: Perform invasion trial
for s in np.linspace(0, 0.5, 11):
    # Reset the list of evolutionarily stable switching rates for each s value
    evolutionarily_stable_switching_rates = []
    
    # Step 4a: Simulate multiple invasion attempts for each s value
    for trial in range(500):
        # Choose mutant mutation rate
        mutant_mutation_rate = mm + random.expovariate(1)
        
        # Step 5: Simulate the population
    for i, variance in enumerate(variances):
        # Perform clonal reproduction
        offspring_major_allele_freq = major_allele_freq
        offspring_modifier_allele_freq = modifier_allele_freq

        # Apply selection
        if environment == "e0":
            w_0_major = 1
            w_0_modifier = 1
            w_1_major = 1 - s_0
            w_1_modifier = 1 - s_0
        else:
            w_0_major = 1 - s_1
            w_0_modifier = 1 - s_1
            w_1_major = 1
            w_1_modifier = 1

        fitness_0 = w_0_major * offspring_major_allele_freq + w_0_modifier * (1 - offspring_major_allele_freq)
        fitness_1 = w_1_major * offspring_major_allele_freq + w_1_modifier * (1 - offspring_major_allele_freq)

        if random.random() < fitness_1 / (fitness_0 + fitness_1):
            offspring_major_allele_freq = 1 - offspring_major_allele_freq

        # Apply mutation
        if random.random() < mm:
            offspring_major_allele_freq = 1 - offspring_major_allele_freq

        if random.random() < mutant_mutation_rate:
            modifier_allele_freq = 1 - modifier_allele_freq

        # Apply environment change
        if random.expovariate(1/mean_waiting_time) > variance:
            if environment == "e0":
                environment = "e1"
            else:
                environment = "e0"

        # Update major and modifier allele frequencies
        major_allele_freq = offspring_major_allele_freq
        modifier_allele_freq = offspring_modifier_allele_freq

            
        # Step 6: Append selected switching rate to list
        if modifier_allele_freq > 10 ** (-4):
            selected_switching_rate = mutant_mutation_rate
        else:
            selected_switching_rate = mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm)
        evolutionarily_stable_switching_rates.append(selected_switching_rate)
        
        # Step 7: Update wild-type mutation rate
        mm = selected_switching_rate
    
    # Step 8: Plot log10 evolution
    x = np.arange(0, 400, 20)
    y = []
    for variance in x:
        selected_switching_rates = []
        for i in range(500):
            # Perform invasion trial
            major_allele_freq = random.uniform(0, 1)
            modifier_allele_freq = 1
            if random.random() < 0.5:
                environment = "e0"
            else:
                environment = "e1"
            mm = 0.1
            for generation in range(1000):
                offspring_major_allele_freq = major_allele_freq
                offspring_modifier_allele_freq = modifier_allele_freq
                if environment == "e0":
                    w_0_major = 1
                    w_0_modifier = 1
                    w_1_major = 1 - s_0
                    w_1_modifier = 1 - s_0
                else:
                    w_0_major = 1 - s_1
                    w_0_modifier = 1 - s_1
                    w_1_major = 1
                    w_1_modifier = 1
                fitness_0 = w_0_major * offspring_major_allele_freq + w_0_modifier * (1 - offspring_major_allele_freq)
                fitness_1 = w_1_major * offspring_major_allele_freq + w_1_modifier * (1 - offspring_major_allele_freq)
                if random.random() < fitness_1 / (fitness_0 + fitness_1):
                    offspring_major_allele_freq = 1 - offspring_major_allele_freq
                if random.random() < mm:
                    offspring_major_allele_freq = 1 - offspring_major_allele_freq
                if random.random() < mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm):
                    modifier_allele_freq = 1 - modifier_allele_freq
                if random.expovariate(variance) > mean_waiting_time:
                    if environment == "e0":
                        environment = "e1"
                    else:
                        environment = "e0"
            if modifier_allele_freq > 10 ** (-4):
                selected_switching_rate = mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm)
            else:
                selected_switching_rate = mm
            selected_switching_rates.append(selected_switching_rate)
        y.append(np.log10(np.mean(selected_switching_rates)))

# Plot the results
ax.scatter(x, y)
# Step 9: Plot dashed line
ax.plot([0, 400], [(1/mean_waiting_time), (1/mean_waiting_time)], '--', color='black', linewidth=1)
ax.set_xlabel("Variance of waiting times")
ax.set_ylabel("Log10 of mean switching rate")
ax.set_title("Effect of waiting time variance on switching rate")
plt.show()


# 1.b. Change something about their model and plot and discuss what happens. For example, you
# can change the fitness matrix and not have opposing selection pressures, as discussed in class.
# Or you can change how the environmental change is modeled. Or you can add recombination
# that is non-zero and see what happens. Or you could make other choices about some thresholds
# they use, such as number of runs to find the ESS or the how to select the new invader mutation
# rate. Anything you may be curious about.

# In[10]:


# Define list to store evolutionarily stable switching rates
evolutionarily_stable_switching_rates = []

# Define mean waiting time
mean_waiting_time = 20

# Define selection coefficients
s = 0.02
s_0 = 0.5
s_1 = 0.1

# Reproduction rate
r = 0.99

# Initialize figure
fig, ax = plt.subplots()

# Define the range of variances of waiting times
variances = np.linspace(0, 400, 20)

# Step 1: Initialize the population with random allele frequencies
major_allele_freq = random.uniform(0, 1)
modifier_allele_freq = 1

# Step 2: Choose the initial environment randomly
if random.random() < 0.5:
    environment = "e0"
else:
    environment = "e1"

# Step 3: Define mutation rates
mM = 0.01
mm = 0.1

# Step 4: Perform invasion trial
for s in np.linspace(0, 0.5, 11):
    # Reset the list of evolutionarily stable switching rates for each s value
    evolutionarily_stable_switching_rates = []
    
    # Step 4a: Simulate multiple invasion attempts for each s value
    for trial in range(500):
        # Choose mutant mutation rate
        mutant_mutation_rate = mm + random.expovariate(1)
        
        # Step 5: Simulate the population
    for i, variance in enumerate(variances):
        # Perform clonal reproduction
        offspring_major_allele_freq = major_allele_freq
        offspring_modifier_allele_freq = modifier_allele_freq

        # Apply selection
        if environment == "e0":
            w_0_major = 1
            w_0_modifier = 1
            w_1_major = 1 - s_0
            w_1_modifier = 1 - s_0
        else:
            w_0_major = 1 - s_1
            w_0_modifier = 1 - s_1
            w_1_major = 1
            w_1_modifier = 1

        fitness_0 = w_0_major * offspring_major_allele_freq * r + w_0_modifier * (1 - offspring_major_allele_freq) * (1-r)
        fitness_1 = w_1_major * offspring_major_allele_freq * r + w_1_modifier * (1 - offspring_major_allele_freq) * (1-r)

        if random.random() < fitness_1 / (fitness_0 + fitness_1):
            offspring_major_allele_freq = 1 - offspring_major_allele_freq

        # Apply mutation
        if random.random() < mm:
            offspring_major_allele_freq = 1 - offspring_major_allele_freq

        if random.random() < mutant_mutation_rate:
            modifier_allele_freq = 1 - modifier_allele_freq

        # Apply environment change
        if random.expovariate(1/mean_waiting_time) > variance:
            if environment == "e0":
                environment = "e1"
            else:
                environment = "e0"

        # Update major and modifier allele frequencies
        major_allele_freq = offspring_major_allele_freq
        modifier_allele_freq = offspring_modifier_allele_freq

            
        # Step 6: Append selected switching rate to list
        if modifier_allele_freq > 10 ** (-4):
            selected_switching_rate = mutant_mutation_rate
        else:
            selected_switching_rate = mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm)
        evolutionarily_stable_switching_rates.append(selected_switching_rate)
        
        # Step 7: Update wild-type mutation rate
        mm = selected_switching_rate
    
    # Step 8: Plot log10 evolution
    x = np.arange(0, 400, 20)
    y = []
    for variance in x:
        selected_switching_rates = []
        for i in range(500):
            # Perform invasion trial
            major_allele_freq = random.uniform(0, 1)
            modifier_allele_freq = 1
            if random.random() < 0.5:
                environment = "e0"
            else:
                environment = "e1"
            mm = 0.1
            for generation in range(2000):
                offspring_major_allele_freq = major_allele_freq
                offspring_modifier_allele_freq = modifier_allele_freq
                if environment == "e0":
                    w_0_major = 1
                    w_0_modifier = 1
                    w_1_major = 1 - s_0
                    w_1_modifier = 1 - s_0
                else:
                    w_0_major = 1 - s_1
                    w_0_modifier = 1 - s_1
                    w_1_major = 1
                    w_1_modifier = 1
                fitness_0 = w_0_major * offspring_major_allele_freq * r + w_0_modifier * (1 - offspring_major_allele_freq) * (1-r)
                fitness_1 = w_1_major * offspring_major_allele_freq * r + w_1_modifier * (1 - offspring_major_allele_freq) * (1-r)
                
                if random.random() < fitness_1 / (fitness_0 + fitness_1):
                    offspring_major_allele_freq = 1 - offspring_major_allele_freq
                if random.random() < mm:
                    offspring_major_allele_freq = 1 - offspring_major_allele_freq
                if random.random() < mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm):
                    modifier_allele_freq = 1 - modifier_allele_freq
                if random.expovariate(variance) > mean_waiting_time:
                    if environment == "e0":
                        environment = "e1"
                    else:
                        environment = "e0"
            if modifier_allele_freq > 10 ** (-4):
                selected_switching_rate = mm + np.exp(-variance / mean_waiting_time) * (1 - 2 * mm)
            else:
                selected_switching_rate = mm
            selected_switching_rates.append(selected_switching_rate)
        y.append(np.log10(np.mean(selected_switching_rates)))

# Plot the results
ax.scatter(x, y)
# Step 9: Plot dashed line
ax.plot([0, 400], [(1/mean_waiting_time), (1/mean_waiting_time)], '--', color='black', linewidth=1)
ax.set_xlabel("Variance of waiting times")
ax.set_ylabel("Log10 of mean switching rate")
ax.set_title("Effect of waiting time variance on switching rate")
plt.show()

