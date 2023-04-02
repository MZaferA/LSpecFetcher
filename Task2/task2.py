#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 17:12:11 2023

@author: zafer
"""

"""
Task 2 extract products from thorlabs:
repeat the exercise from before but for thorlabs.
use the following link to extract information from plano convex lenses
https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3279
Thorlabs might present some challenges while retrieving the information using simple tools like request.
- could you identify the problem and find a solution? 
- if you don't manage to automate the process of retrieving the information from the server, can you find a manual way to retrieve the information of the html that you see after clicking in the link and then process it in python?


"""

#import the required libraries: here I use requests and BeautifulSoup as suggested in the task description
from bs4 import BeautifulSoup
import requests
import json
import sys


########################
address = 'https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=3279'
#######################




#Define helper functions for data cleaning
def clean_data(table):
    value = table.findChild('td', {'align': 'center'}).get_text(strip=True).replace('\xa0', ' ') 
    
    if 'J/cm2' in value:
        return value.replace('J/cm2', 'J/cm<sup>2</sup> ')
    
    sup = table.findChild('td', {'align':'center'}).findChild('sup')
    
    if sup is not None:
        value = value[:value.rfind(sup.text)]
        
    return value

def clean_data_body(element):
    value = element.get_text(strip=True)
    sup = element.findChild('sup')
    
    if sup is not None:
        value = value[:value.rfind(sup.text)]
        
    return value


#Try to load the webpage: if error ->No need to proceed, just terminate
try:
    with requests.Session() as session:
        page = session.get(address)
        contents = page.content
except:
    print('Problems with the requested webpage, terminating...')
    sys.exit()


#Load BeautifulSoup: if error -> terminate
try:
    soup = BeautifulSoup(contents, 'html.parser')
    container = soup.find_all("div", {"id": "sgContainer"})[0].find_all('div', {'class':'SubGroup'})  
except:
    print('BeautifulSoup is out, terminating...')
    sys.exit()
    
    
components = []


#Find the spec table
#This table shows the shared specs for this family of lenses
table = soup.findChild('div', {'id': 'tabContainer'}).findChild('table', {'class': 'SpecTable'}).findChild('tbody')

#Extract the rest of the required data
table =  table.find_next('tr').find_next('tr')
lens_shape = clean_data(table)

table =  table.find_next('tr')
material = clean_data(table)

table =  table.find_next('tr')
ar_coating = clean_data(table)

table =  table.find_next('tr')
reflectance_range = clean_data(table)

table =  table.find_next('tr')
design_wavelength = clean_data(table)

table =  table.find_next('tr')
refractive_index = clean_data(table)

table =  table.find_next('tr')
surface_flatness = clean_data(table)

table =  table.find_next('tr')
spherical_surface_power = clean_data(table)

table =  table.find_next('tr')
surface_irregularity = clean_data(table)

table =  table.find_next('tr').find_next('tr').find_next('tr').find_next('tr').find_next('tr')
damage_threshold = clean_data(table)

table =  table.find_next('tr')
abbe_number = clean_data(table)

table =  table.find_next('tr')
clear_aperture = clean_data(table)

table =  table.find_next('tr')
focal_length_tolerance = clean_data(table)


# Thorlabs webpage is pretty much structured: contains bundles of data
for bundle in container:   
    item = {}
    
    #Extract the elements in the current bundle
    elements = bundle.findChild('table', {'class':'SpecTable'}).findChild('tbody').find_all('tr')
   
    found_ref_pic = False
    
    #Iterate over all elements and extract the data
    for element in elements:
        try:
            element = element.find_next('td')
            item_id = clean_data_body(element)
            element = element.find_next('td')
            diameter = element.get_text(strip=True)
            element = element.find_next('td')
            focal_length = element.get_text(strip=True)
            element = element.find_next('td')
            diopter = element.get_text(strip=True)
            element = element.find_next('td')
            radius_of_curvature = element.get_text(strip=True)
            element = element.find_next('td')
            center_thickness = element.get_text(strip=True)
            element = element.find_next('td')
            edge_thickness = element.get_text(strip=True)
            element = element.find_next('td')
            back_focal_length = element.get_text(strip=True)
            element = element.find_next('td')
            
            #Reference drawing is shared among the lenses in the same bundle, so once retrieve is enough
            #The rest of the calls will throw an exception and we will just continue as if nothing happened
            try:
                reference_drawing = 'https://www.thorlabs.com/' +element.findChild('a')['href']
            except:
                pass
            
            #Form the item with the obtained data
            item = {
                'thorlabs/' + item_id:
                {
                    "Back Focal Length (mm)": back_focal_length,
                    "Center Thickness (mm)": center_thickness,
                    "Diameter (mm)": diameter,
                    "Diopter": diopter,
                    "Edge Thickness (mm)": edge_thickness,
                    "Focal Length (mm)": focal_length,
                    "Radius of Curvature (mm)": radius_of_curvature,
                    "Reference Drawing": reference_drawing,
                    "Damage Threshold": damage_threshold,

                    "AR Coating Range": ar_coating,
                    "Abbe Number": abbe_number,
                    "Clear Aperture": clear_aperture,
                    "Design Wavelength": design_wavelength,
                    "Focal Length Tolerance": focal_length_tolerance,
                    "Index of Refraction": refractive_index,
                    "Lens Shape": lens_shape,
                    "Spherical Surface Power (Convex Side)": spherical_surface_power,
                    "Substrate Material": material,
                    "Surface Flatness (Plano Side)": surface_flatness,
                    "Surface Irregularity (Peak to Valley)": surface_irregularity,
                    "Reflectance over Coating Range (Avg.) @ 0° AOI": reflectance_range,
                },
            }
                   
            #Try to add it to the component list
            #Ideally this should never throw an exception, but just in case we check it
            try:
                components.append(item)
            except:
                #If error -> just terminate for the current verion
                #In the next verions error-specific actions can be taken, such as memory overflow, etc.
                print('Cannot append to item list, terminating...')
                sys.exit()
                
        except:
            #This should not err ideally.
            #If it fires, most probably they changed the structure of the webpage 
            print('Unexpected structure in the retrived html file')
            
            
#Last try to save the data in json format
try:
    with open("./Task2/task2.json", "w") as outfile:
        json.dump(components, outfile, ensure_ascii=False)
except:
    #If error -> probably a folder access issue, inform the user and terminate for now.
    #In the next version, one can determine the error type and can take actions accordingly
    print('Cannot save the file, do you have access to the destination folder?')
    sys.exit()    
    
    
    