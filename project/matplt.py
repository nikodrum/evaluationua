# -*- coding: UTF-8 -*-
#from sklearn.linear_model import LinearRegression
#from sklearn.cross_validation import train_test_split
#import numpy as np
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt

trans = {'price':u'Цена',
         'room':u'Количество комнат',
         'all_area':u'Общая площадь',
         'livin_area':u'Жилая площадь',
         'kitch_area':u'Площадь кухни',
         'all_floors':u'Количество этажей в доме',
         'year':u'Год постройки'}

def plot_hist(data_for_plot):


#making data

    metr_data_hist = []

    metr_name_hist = data_for_plot[0][0]
    for i in data_for_plot[0][1]:
        try :
            metr_data_hist.append(float(i))
        except ValueError:
            pass
    
#    rc('font', **font)

#histogram

    plt.figure(figsize=(12, 9))    
    plt.style.use('ggplot')

# change range for each plot
    plt.hist(metr_data_hist,bins=40)
# change coords for text
    #plt.text(0,0,"Data source: www.lun.ua | Author: Nikolai Yakovlev (@nikoodrum)", fontsize=10)
    
    f = tempfile.NamedTemporaryFile(dir='project/static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng1 = f.name.split('temp')[-1]
    return [plotPng1,trans[metr_name_hist]]

def plot_scatter(data_for_plot):

#making data

    metr_data_scatter_x = []
    metr_data_scatter_y = []
    metr_data_scatter = []
    metr_data_scatter_x_cl = []
    metr_data_scatter_y_cl = []

    metr_name_scatter_x = data_for_plot[1][0]
    metr_name_scatter_y = data_for_plot[2][0]
    metr_data_scatter_x = data_for_plot[1][1]
    metr_data_scatter_y = data_for_plot[2][1]
    
    for i in range(0,len(metr_data_scatter_x)):
        metr_data_scatter.append([metr_data_scatter_x[i],metr_data_scatter_y[i]])
    for i in range(0,len(metr_data_scatter)):
        if '' not in metr_data_scatter[i]:
            metr_data_scatter_x_cl.append(metr_data_scatter[i][0])
            metr_data_scatter_y_cl.append(metr_data_scatter[i][1])
    X_train = metr_data_scatter_x_cl
    y_train = metr_data_scatter_y_cl
#    r=''
#    y_train=0
    
#    if metr_name_scatter_x != 'year' and metr_name_scatter_y != 'year':

#        X_train, X_test, y_train, y_test = train_test_split(metr_data_scatter_x_cl,metr_data_scatter_y_cl)
#        X_train = np.array(X_train).reshape(len(X_train),1)
#        y_train = np.array(y_train).reshape(len(y_train),1)
#        X_test = np.array(X_test).reshape(len(X_test),1)
#        y_test = np.array(y_test).reshape(len(y_test),1)

#regression

#        regressor = LinearRegression()
#        regressor.fit((X_train), (y_train))
#        xx = np.linspace(0, max(metr_data_scatter_x_cl))
#        yy = regressor.predict(xx.reshape(xx.shape[0], 1))
#        r = 'R^2=' + str(int(regressor.score(X_test,y_test)*100)) + '%'

#scatter

    plt.figure(figsize=(12, 9))
#    plt.plot(xx, yy)
    plt.style.use('ggplot')
    plt.yticks(fontsize=14)  
    plt.xticks(fontsize=14)  

#    plt.text(0,max(y_train),r, fontsize=15)

    plt.scatter(X_train, y_train,color = 'black', alpha=0.4)
    f = tempfile.NamedTemporaryFile(dir='project/static/temp',suffix='.png',delete=False)
    plt.savefig(f)
    f.close()
    plotPng2 = f.name.split('temp')[-1]
    return [str(plotPng2),trans[metr_name_scatter_x],trans[metr_name_scatter_y]]

    #print (metr_data_scatter_x_cl[0:10])        
    #print (metr_data_scatter_y_cl[0:10])        
    
#    rc('font', **font)
#    regressor = LinearRegression()
