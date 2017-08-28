"""
Plotting graph of number of posts against amount of users active
on said post. Further statistical analysis to be performed

Fits including power law, lognormal, stretched exponential and exponential analysed

Options at beginning allow choice of facebook page, time frame and required fits

29.06.17
DewiGould

"""

import numpy as np
import powerlaw
import pandas as pd
import matplotlib.pyplot as plt

#CHOOSE DATA

#look at data from UB, ICL, MIT, SU
University = "SU"
#Previous 18months =1, 2014-2015=2, 
TimeFrame = "1"
#hist, power, lognormal, exp,strexp, all
graph_type = "lognormal"





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
    if TimeFrame == "1":
	plt.title('%s. January 2016 - Present' %(University))
    if TimeFrame == "2":
	plt.title('%s. July 2014 - December 2015' %(University))
    plt.xlabel('User engagement per post')
    plt.ylabel('Number of Posts')
    plt.show()
    return num_engagement, num_posts


#Import information for required University and Timeframe
if University == "UB":
	
	Location4 = '/home/dewigould/Documents/Comparison/UB/UB01012016-30062016/page_124038361034_2017_06_28_11_50_20_fullstats.tab'
        Location5= '/home/dewigould/Documents/Comparison/UB/UB01072016-31122016/page_124038361034_2017_06_28_11_47_37_fullstats.tab'
        Location6= '/home/dewigould/Documents/Comparison/UB/UB01012017-27062017/page_124038361034_2017_06_28_11_42_10_fullstats.tab'
	Location1 = '/home/dewigould/Documents/Comparison/UB/UB01072014-31122014/page_124038361034_2017_07_03_10_22_59_fullstats.tab'
        Location2 = '/home/dewigould/Documents/Comparison/UB/UB01012015-30062015/page_124038361034_2017_07_03_10_18_45_fullstats.tab'
        Location3 = '/home/dewigould/Documents/Comparison/UB/UB01072015-311215/page_124038361034_2017_07_03_10_13_05_fullstats.tab'
if University == "ICL":
        Location4 = '/home/dewigould/Documents/Comparison/ICL/ICL01012016-30062016/page_148242696837_2017_06_28_12_11_31_fullstats.tab'
        Location5= '/home/dewigould/Documents/Comparison/ICL/ICL01072016-31122016/page_148242696837_2017_06_28_12_03_16_fullstats.tab'
        Location6= '/home/dewigould/Documents/Comparison/ICL/ICL01072016-31122016/page_148242696837_2017_06_28_12_03_16_fullstats.tab'
        Location1 ='/home/dewigould/Documents/Comparison/ICL/ICL01072014-31122014/page_148242696837_2017_07_03_10_37_47_fullstats.tab'
        Location2 = '/home/dewigould/Documents/Comparison/ICL/ICL01012015-30062015/page_148242696837_2017_07_03_10_41_20_fullstats.tab'
        Location3 = '/home/dewigould/Documents/Comparison/ICL/ICL01072015-31122015/page_148242696837_2017_07_03_10_45_34_fullstats.tab'
if University == "MIT":
        Location4 = '/home/dewigould/Documents/Comparison/MIT/MIT01012016-30062016/page_126533127390327_2017_06_28_12_39_35_fullstats.tab'
        Location5= '/home/dewigould/Documents/Comparison/MIT/MIT01072016-31122016/page_126533127390327_2017_06_28_12_29_31_fullstats.tab'
        Location6= '/home/dewigould/Documents/Comparison/MIT/MIT01012017-27062017/page_126533127390327_2017_06_28_12_18_33_fullstats.tab'
        Location1 = '/home/dewigould/Documents/Comparison/MIT/MIT01072014-31122014/page_126533127390327_2017_07_03_10_56_39_fullstats.tab'
        Location2 = '/home/dewigould/Documents/Comparison/MIT/MIT01012015-30062015/page_126533127390327_2017_07_03_11_04_12_fullstats.tab'
        Location3 = '/home/dewigould/Documents/Comparison/MIT/MIT01072015-31122015/page_126533127390327_2017_07_03_11_09_31_fullstats.tab'
if University == "SU":
	Location1 = '/home/dewigould/Documents/Comparison/SU/SU01072014-31122014/page_6192688417_2017_07_10_12_28_25_fullstats.tab'
	Location2 = '/home/dewigould/Documents/Comparison/SU/SU01012015-30062015/page_6192688417_2017_07_10_12_24_03_fullstats.tab'
	Location3 = '/home/dewigould/Documents/Comparison/SU/SU01072015-31122015/page_6192688417_2017_07_10_12_20_55_fullstats.tab'
	Location4 = '/home/dewigould/Documents/Comparison/SU/SU01012016-30062016/page_6192688417_2017_07_10_12_17_01_fullstats.tab'
	Location5= '/home/dewigould/Documents/Comparison/SU/SU01072016-31122016/page_6192688417_2017_07_10_12_12_39_fullstats.tab'
	Location6 = '/home/dewigould/Documents/Comparison/SU/SU01012017-27062017/page_6192688417_2017_07_10_12_06_51_fullstats.tab'

if TimeFrame == "1":
	Locations_added = [Location4, Location5, Location6]
if TimeFrame == "2":
	Locations_added = [Location1, Location2, Location3]
        
#function to combine data over individual 6month periods
def combine_data(Locations):
	data=[]
	for i in Locations:
		data_i = engagement_numbers(Location1)
		for j in data_i:
			data.append(j)
	return data

produce_data(combine_data(Locations_added))

	

















    
