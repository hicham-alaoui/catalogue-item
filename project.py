from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from properteez_db import Base, Area, CatalogItem

import cgi
app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///properteez_list.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#all areas
@app.route('/')
@app.route('/areas/')
def allAreas():
	
    	all_areas = session.query(Area).all()
    	return render_template('all_areas.html', area=all_areas)

#new area
@app.route('/areas/new', methods=['GET','POST'])
def newArea():
	if request.method == 'POST':
		newarea = Area(name = request.form['name'])
		session.add(newarea)
		session.commit()
		return redirect(url_for('allAreas'))
	else:
		return render_template('new_area.html')

#edit area
@app.route('/areas/<int:area_id>/edit', methods=['GET','POST'])
def editArea(area_id):
	editarea = session.query(Area).filter_by(area_id=area.id).one()
	if request.method == 'POST':
		if request.form['name']:
			editarea.name = request.form['name']
			session.add(editarea)
			session.commit()
			return redirect(url_for('allAreas'))
	else:
		return render_template('edit_area.html')

#single area method
@app.route('/area/<int:area_id>/')
def myAreas(area_id):
    #area = session.query(Area).all()
    areas = session.query(Area).filter_by(id = area_id).one()
    properties = session.query(CatalogItem).filter_by(area_id = area_id)
    return render_template('single_area.html', area=areas, properties=properties)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)