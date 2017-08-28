"""
Compare Historical Data, + fits for different Uni's on one plot

29.06.17
DewiGould

"""

import numpy as np
import powerlaw
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

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


label_one = ["UB fit","ICL fit", "MIT fit"]
label_two = ["UB data", "ICL fit", "MIT, fit"]
count = np.arange(1,19)
def produce_data(engagement_data_input):
	for i in count:
		engagement_data_input[i-1].sort()
		engagement_data = engagement_data_input[i-1]
		data = Counter(engagement_data)
		num_engagement= data.keys()
    		num_posts= data.values()

    		d=np.array(num_engagement)
    		fit = powerlaw.Fit(d,discrete=True,xmin=5)
    		#fit.lognormal.plot_pdf(color='b', linestyle='--',label='Lognormal fit. Mu = %s, sigma = %s'%(round(fit.lognormal.mu,3),round(fit.lognormal.sigma,3)))
		fit.lognormal.plot_pdf(color='b', linestyle='--')
    		#fit.plot_pdf()
        plt.xlabel('User engagement per post')
        plt.ylabel('Number of Posts')
	plt.legend(loc='best')
        plt.show()
        return num_engagement, num_posts


#Import information for required University and Timeframe

#UB
Location4 = '/home/dewigould/Documents/Comparison/UB/UB01012016-30062016/page_124038361034_2017_06_28_11_50_20_fullstats.tab'
Location5= '/home/dewigould/Documents/Comparison/UB/UB01072016-31122016/page_124038361034_2017_06_28_11_47_37_fullstats.tab'
Location6= '/home/dewigould/Documents/Comparison/UB/UB01012017-27062017/page_124038361034_2017_06_28_11_42_10_fullstats.tab'
Location1 = '/home/dewigould/Documents/Comparison/UB/UB01072014-31122014/page_124038361034_2017_07_03_10_22_59_fullstats.tab'
Location2 = '/home/dewigould/Documents/Comparison/UB/UB01012015-30062015/page_124038361034_2017_07_03_10_18_45_fullstats.tab'
Location3 = '/home/dewigould/Documents/Comparison/UB/UB01072015-311215/page_124038361034_2017_07_03_10_13_05_fullstats.tab'
#ICL
Location10 = '/home/dewigould/Documents/Comparison/ICL/ICL01012016-30062016/page_148242696837_2017_06_28_12_11_31_fullstats.tab'
Location11= '/home/dewigould/Documents/Comparison/ICL/ICL01072016-31122016/page_148242696837_2017_06_28_12_03_16_fullstats.tab'
Location12= '/home/dewigould/Documents/Comparison/ICL/ICL01072016-31122016/page_148242696837_2017_06_28_12_03_16_fullstats.tab'
Location7 ='/home/dewigould/Documents/Comparison/ICL/ICL01072014-31122014/page_148242696837_2017_07_03_10_37_47_fullstats.tab'
Location8 = '/home/dewigould/Documents/Comparison/ICL/ICL01012015-30062015/page_148242696837_2017_07_03_10_41_20_fullstats.tab'
Location9 = '/home/dewigould/Documents/Comparison/ICL/ICL01072015-31122015/page_148242696837_2017_07_03_10_45_34_fullstats.tab'
#MIT
Location16 = '/home/dewigould/Documents/Comparison/MIT/MIT01012016-30062016/page_126533127390327_2017_06_28_12_39_35_fullstats.tab'
Location17= '/home/dewigould/Documents/Comparison/MIT/MIT01072016-31122016/page_126533127390327_2017_06_28_12_29_31_fullstats.tab'
Location18= '/home/dewigould/Documents/Comparison/MIT/MIT01012017-27062017/page_126533127390327_2017_06_28_12_18_33_fullstats.tab'
Location13 = '/home/dewigould/Documents/Comparison/MIT/MIT01072014-31122014/page_126533127390327_2017_07_03_10_56_39_fullstats.tab'
Location14 = '/home/dewigould/Documents/Comparison/MIT/MIT01012015-30062015/page_126533127390327_2017_07_03_11_04_12_fullstats.tab'
Location15 = '/home/dewigould/Documents/Comparison/MIT/MIT01072015-31122015/page_126533127390327_2017_07_03_11_09_31_fullstats.tab'

Locations_all = [[Location1,Location2,Location3],[Location4,Location5,Location6],[Location7,Location8,Location9],[Location10,Location11,Location12],[Location13,Location14,Location15],[Location16, Location17,Location18]]

        
#function to combine data over individual 6month periods

def combine_data(Locations):
	all_data= []
	for group in Locations:
		data_group = []
		for location in group:
			data_i = engagement_numbers(location)
			for j in data_i:
				data_group.append(j)
			all_data.append(data_group)
	return all_data


result = combine_data(Locations_all)
produce_data(result)
















    
