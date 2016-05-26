# -*- coding: UTF-8 -*-
from flask import g, render_template, redirect, url_for, session, request
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from project import models as md
from project import forms
from project import app
from project import database as db


@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():

    md.clean_temp_folder('project/static/temp')

    form = forms.MyForm()
    if form.validate_on_submit():

        lat = md.calculating(form.street.data,form.num_build.data)[0]
        lon = md.calculating(form.street.data,form.num_build.data)[1]
        
        valid_data  = md.data_validation([lat,lon,form.year.data,form.room.data,form.all_area.data,form.all_floors.data])
        db.insert_db(form.street.data,valid_data[0],valid_data[1],valid_data[2],valid_data[3],valid_data[4],valid_data[5])

        return redirect('/result')
    return render_template('index.html', form=form)

@app.route('/result', methods = ['GET','POST'])
def result():
    form = forms.MyForm_result()

    search_result = db.search_db()
    varian_of_similarity = 0        
    posts_cl = search_result[0]

    if len(search_result[1]) != 0:

        posts_my_data = md.choose_full_info_row(search_result[1])

        if posts_my_data != None :

            data_for_plot = db.taking_data_for_plot(posts_my_data['distr'])
            path_imgs = md.plotting(data_for_plot)

            path_img_hist = '../static/temp/' + path_imgs[0][1:]
            path_img_scatter = '../static/temp/' + path_imgs[1][1:]
            varian_of_similarity = 1

            return render_template('result.html',variant=varian_of_similarity, posts_cl = posts_cl,my_data = 
            posts_my_data,plotPng1=path_img_hist,plotPng2=path_img_scatter, form=form, labels = path_imgs[2])
    else :

        posts_my_data = 'Мы не нашли похожую на рынке. Ваша квартира уникана!'  
        path_img_hist = '../static/img/index_plot.png'
        path_img_scatter = '../static/img/index_plot.png'
        varian_of_similarity = 0
        return render_template('result.html',variant=varian_of_similarity, posts_cl = posts_cl,my_data = 
            posts_my_data,plotPng1=path_img_hist,plotPng2=path_img_scatter,form=form)


@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(400)

def internal_error(error):
    return render_template('error.html')