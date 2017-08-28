"""


DewiGould

"""

import numpy as np
import powerlaw
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


graph_type = "all"

location_GB = '/home/dewigould/Documents/PROJECT/GB/page_140123476092919_2017_07_18_11_21_03_fullstats.tab'
location_GC = '/home/dewigould/Documents/PROJECT/GC/page_552083274809379_2017_07_18_11_24_00_fullstats.tab'
location_TP = '/home/dewigould/Documents/PROJECT/TP/page_46727363062_2017_07_18_11_26_57_fullstats.tab'
location_CH = '/home/dewigould/Documents/PROJECT/CH/'
location_TV = '/home/dewigould/Documents/PROJECT/TV/'
location_FM = '/home/dewigould/Documents/PROJECT/FM/'
location_TA = '/home/dewigould/Documents/PROJECT/TA/'
location_RR = '/home/dewigould/Documents/PROJECT/RR/'
location_QF = '/home/dewigould/Documents/PROJECT/QF/'
location_DB = '/home/dewigould/Documents/PROJECT/DB/'
location_LF = '/home/dewigould/Documents/PROJECT/LF/'
location_DM = '/home/dewigould/Documents/PROJECT/DM/'
location_SK = '/home/dewigould/Documents/PROJECT/SK/'
location_NT = '/home/dewigould/Documents/PROJECT/NT/'


location_TX = '/home/dewigould/Documents/PROJECT/Barcelona/TX/page_157248094325296_2017_07_18_12_45_57_fullstats.tab'
location_EL = '/home/dewigould/Documents/PROJECT/Barcelona/EL/page_35735977639_2017_07_18_12_48_07_fullstats.tab'
location_BL = '/home/dewigould/Documents/PROJECT/Barcelona/BL/page_242544625792496_2017_07_18_12_49_29_fullstats.tab'
location_DP = '/home/dewigould/Documents/PROJECT/Barcelona/DP/'
location_SC = '/home/dewigould/Documents/PROJECT/Barcelona/SC/'
location_EC = '/home/dewigould/Documents/PROJECT/Barcelona/EC/'
location_GO = '/home/dewigould/Documents/PROJECT/Barcelona/GO/'
location_BH = '/home/dewigould/Documents/PROJECT/Barcelona/BH/'
location_ML = '/home/dewigould/Documents/PROJECT/Barcelona/ML/'
location_JD = '/home/dewigould/Documents/PROJECT/Barcelona/JD/'
location_LB = '/home/dewigould/Documents/PROJECT/Barcelona/LB/'
location_IB = '/home/dewigould/Documents/PROJECT/Barcelona/IB/'
location_AF = '/home/dewigould/Documents/PROJECT/Barcelona/AF/'
location_LI = '/home/dewigould/Documents/PROJECT/Barcelona/LI/'
location_EP = '/home/dewigould/Documents/PROJECT/Barcelona/EP/'



def engagement_numbers(Location):

    #create dataframe
    df_raw= pd.read_table(Location)
    engagement=df_raw['engagement_fb']

    #create array of engagement numbers
    engagement_numbers=[]
    for i in range(len(df_raw)):
        engagement_numbers.append(engagement[i])
    #print "engagement numbers: ", engagement_numbers
    return engagement_numbers

def produce_data(engagement_data_input):
    engagement_data_input.sort()
    #remove large values to look at small behaviour
    #engagement_data = [s for s in engagement_data_input if s<=8000]
    #or include all data
    engagement_data=engagement_data_input
    from collections import Counter
    #Dictionary with engagement numbers and number of posts with those numbers
    data = Counter(engagement_data)
    #print "Counter Data: ", data
    data.most_common()
    #print "Number of users and associated number of pages", data
    num_engagement= data.keys()
    num_posts= data.values()
    print "Total Posts: ", sum(num_posts)
    total_num =0.
    for i in num_posts:
    	total_num += i
    probability = np.array(num_engagement)/total_num
    #print probability  
    #print "Processed Engagement numbers", num_engagement
    
    #R is the loglikelihood ratio between the two candidate distributions. This number will be positive
    #if the data is more likely in the first distribution, and negative if the data is more likely in the second
    #distribution

    #p value indicates whether or not to reject null hypothesis (distribution under comparison), reject null if
    # p value <0.05

    #set xmin either as value of (,)...include more or less of data


    if graph_type == "all":
        d=np.array(num_engagement)
	fit = powerlaw.Fit(d,discrete=True,xmin=5)
        fit.power_law.plot_pdf(color='b',linestyle='--',label='Power law fit. Alpha = %s, sigma = %s'%(round(fit.power_law.alpha,3),round(fit.power_law.sigma,3)))
	fit.exponential.plot_pdf(color='r',linestyle='--',label='Exponential fit')
	fit.lognormal.plot_pdf(color='g',linestyle='--',label='Lognormal fit. Mu = %s, sigma = %s'%(round(fit.lognormal.mu,3),round(fit.lognormal.sigma,3)))
	fit.stretched_exponential.plot_pdf(color='y',linestyle='--', label= 'Stretched exponential fit')
	fit.plot_pdf(color='k',label='Empirical Data')
	plt.legend(loc = 'best')


        
	print "Power Law: "
	R,p = fit.distribution_compare("power_law","exponential", normalized_ratio=True)
	print "power law vs exponential: ", R,p
	print('alpha= ',fit.power_law.alpha,'  sigma= ',fit.power_law.sigma) 

	print "Lognormal: "
    	R1, p1 = fit.distribution_compare("lognormal","power_law",normalized_ratio=True)
    	print "lognormal vs power_law: ",R1,p1
#mu and sigma are standard parameters of Gaussian distribution (lognormal is Gaussian when log taken)
        mu=fit.lognormal.mu
        sigma=fit.lognormal.sigma
        D=fit.lognormal.D
        print "log-normal: mu=",mu,"sigma=",sigma
	print "log-normal, D: ", D

	print "stretched exponential: "
	print "strech_exp, D: ", fit.stretched_exponential.D
    
    	R2, p2 = fit.distribution_compare("stretched_exponential","lognormal",normalized_ratio=True)
    	print "stretched exponential vs lognormal: ",R2,p2
	R3,p3 = fit.distribution_compare("stretched_exponential", "power_law",normalized_ratio=True)
	print "stretched exponential vs power law", R3,p3


    if graph_type == "power":
    	d=np.array(num_engagement)
    	#fit = powerlaw.Fit(d, discrete=True, estimate_discrete=True)

    	fit = powerlaw.Fit(d,discrete=True,xmin=5)
    	fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit pdf')
    	fit.plot_pdf(color= 'r')
	R,p = fit.distribution_compare("power_law","exponential", normalized_ratio=True)
	print "power law vs exponential: ", R,p

    	print('alpha= ',fit.power_law.alpha,'  sigma= ',fit.power_law.sigma)  

    if graph_type == "lognormal":
	d=np.array(num_engagement)
	fit = powerlaw.Fit(d,discrete=True,xmin=5)
	fit.lognormal.plot_pdf(color='b', linestyle='--', label='fit pdf')
	fit.plot_pdf(color='r')
	print "lognormal, D: ", fit.lognormal.D
    
    	R0, p = fit.distribution_compare("lognormal","power_law",normalized_ratio=True)
    	print "lognormal vs power_law: ",R0,p
        mu=fit.lognormal.mu
        sigma=fit.lognormal.sigma
        D=fit.lognormal.D
        print "log-normal: mu=",mu,"sigma=",sigma
    
    if graph_type == "exp":
	d=np.array(num_engagement)
	fit = powerlaw.Fit(d,discrete=True,xmin=5)
	fit.exponential.plot_pdf(color='b', linestyle='--', label='fit pdf')
	fit.plot_pdf(color='r')
	print "exponential, D: ", fit.exponential.D
    
    	R0, p = fit.distribution_compare("exponential", "lognormal",normalized_ratio=True)
    	print "exponential vs lognormal: ",R0,p

    #stretched exponential is f(t)=e^(t^b) where b is FRACTIONAL
    if graph_type== "strexp":
    	d=np.array(num_engagement)
	fit = powerlaw.Fit(d,discrete=True,xmin=5)
	fit.stretched_exponential.plot_pdf(color='b', linestyle='--', label='fit pdf')
	fit.plot_pdf(color='r')
	print "strech_exp, D: ", fit.stretched_exponential.D
    
    	R0, p = fit.distribution_compare("stretched_exponential","exponential",normalized_ratio=True)
    	print "stretched exponential vs exponential: ",R0,p
    
    if graph_type == "hist":

    	#Plot
    	plt.hist(num_engagement)

    plt.xlabel('User engagement per post')
    plt.ylabel('Number of Posts')
    plt.show()
    return num_engagement, num_posts


produce_data(engagement_numbers(location_TX))

