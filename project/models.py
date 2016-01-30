# -*- coding: UTF-8 -*-
from random import randint
import math
from project import matplt,database
from geopy.geocoders import Nominatim
from geopy import exc
import os, shutil


categ_coef = 17960
geolocator = Nominatim()


def clean_temp_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def data_validation(list_data_for_valid):
    for i in list_data_for_valid:
        try:
            i = float(i)
        except ValueError:
            i = 0
    return list_data_for_valid



def plotting(post_plot_distr):

# collecting data for plot

    metrics = ['price','room','all_area','livin_area','kitch_area','all_floors','year']
    to_return_plot_data = []

    for i in range(3):
        num_of_metr = randint(0,len(metrics)-1)
        plt_data = []
        for i in range(0,len(post_plot_distr)): 
            try :
                plt_data.append(post_plot_distr[i][metrics[num_of_metr]])
            except IndexError:
                break
        to_return_plot_data.append([metrics[num_of_metr],plt_data])
        metrics.remove(metrics[num_of_metr])

    path_img_hist =  matplt.plot_hist(to_return_plot_data)    
    path_img_scatter = matplt.plot_scatter(to_return_plot_data)

    return [path_img_hist[0],path_img_scatter[0],[path_img_hist[1],path_img_scatter[1],path_img_scatter[2]]]
 
def calculating(street,num_build):
    location = None
    try:
        location = geolocator.geocode("Киев, " + street +' '+ num_build )
        if location != None:
            lat = location.latitude
            lon = location.longitude
        else :
            lat = 0
            lon = 0
    except exc.GeocoderTimedOut:
        lat = 0
        lon = 0

    return [lat,lon]

def choose_full_info_row(list_df_na):
    indicator = False
    data_for_posting = None
    while indicator == False:     
        rand_n = randint(0,len(list_df_na))
        try:
            if list_df_na[rand_n]['price'] != '' and list_df_na[rand_n]['street'] != ''and list_df_na[rand_n]['distr'] != ''and list_df_na[rand_n]['all_area'] != ''and list_df_na[rand_n]['all_floors'] != ''and list_df_na[rand_n]['room'] != '':
                data_for_posting = list_df_na[rand_n]
                indicator = True
        except IndexError:
            indicator = True
    return data_for_posting
