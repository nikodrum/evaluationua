# -*- coding: UTF-8 -*-
from flask import g
import sqlite3
import math

database = "project/appart.db"

categ_coef = 17960
coef = 360/6378137
def connect_db():
    return sqlite3.connect(database)

def insert_db(street,lat,lon,year,room,all_area,all_floors):

# validating wether coordinates in Kyiv
#calculating distances

    if lat < 50.702443 and lat > 50.144912:
        if lon > 30.225671 and lon < 30.935312:
            len_to_center_in_coord = ((lat-50.450198)**2+(lon-30.523986)**2)**(1/2)
            len_to_center = len_to_center_in_coord/coef
            len_to_metro = def_nearest_subway(lat,lon)
    else:
        len_to_center = 0
        len_to_metro = 0

# calculating data for building of price estimation 

    client_price = int(math.exp(7.483156+ 0.001652*float(year)
                                        + 0.122520*float(room)
                                        + 0.008478*float(all_area)
                                        + 0.007029*float(all_floors)
                                        - 0.000286*float(len_to_center)
                                        - 0.000407*float(len_to_metro)))

    category = int((client_price)/categ_coef)

# inserting data to DB    

    data_list = [street,lat,lon,year,room,all_area,all_floors,client_price,category,len_to_center*6.283279]
    g.db = connect_db()
    cur = g.db.cursor()
    cur.execute('INSERT INTO client_data VALUES (?,?,?,?,?,?,?,?,?,?)',data_list)
    g.db.commit()

    return g.db.close()

# taking from database info  

def search_db():
    g.db = connect_db()
    cur = g.db.cursor()

# taking client data 

    client_row = cur.execute('SELECT * FROM client_data WHERE ROWID=(SELECT MAX(ROWID) FROM client_data)')
    posts_cl = []
    posts_cl = [dict(year = row[3],room=row[4],all_area=row[5],all_floors=row[6],cl_price=row[7],category=row[8]) for row in client_row.fetchall()]

# taking data from calculated category based on price estimation      

    category = posts_cl[0]['category']
    if category == 0: 
        category = 1
    my_data_row = cur.execute('SELECT * FROM mytable_na WHERE price_category = (?)',[category])
    posts_my_data=[]
    posts_my_data = [dict(price=row[3],street=row[0],room=row[5],all_area=row[6],all_floors=row[9],distr=row[12]) for row in my_data_row.fetchall()]
    g.db.close() 
    return [posts_cl,posts_my_data]

def taking_data_for_plot(rand_district):

    g.db = connect_db()
    cur = g.db.cursor()

# taking all data with district which was choosen in my data
#7 differnt metrics of districts

    distr_data = cur.execute('SELECT * FROM mytable_na WHERE distr = (?)',[rand_district])    
    post_plot_distr = [dict(price = row[3],room = row[5],all_area=row[6],livin_area=row[7],kitch_area=row[8],all_floors=row[9],year=row[11],distr=str(row[13])) for row in distr_data.fetchall()]
    g.db.close() 
    return post_plot_distr

def def_nearest_subway(lat,lon):

    g.db = connect_db()
    cur = g.db.cursor()

# taking metro data 

    client_row = cur.execute('SELECT * FROM metro_coords ')
    metro_coords = []
    for row in client_row.fetchall():
        metro_coords.append([row[0],row[1],row[2]]) 
    g.db.close() 

    min_list = []

    for i in range(0,len(metro_coords)):

        min_list.append((((lat - metro_coords[i][1])**2+(lon - metro_coords[i][2]))**2)**(1/2))

    min_val = None
    for i in range(0,len(min_list)) :
        if min_val is None or min_list[i] < min_val :
            min_val = min_list[i]

    return min_val/coef