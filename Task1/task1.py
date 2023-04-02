#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 15:47:51 2023

@author: zafer
"""

"""
Task 1 extract products from optosigma optics:
extract the plano convex lenses listed in this link:
https://www.optosigma.com/eu_en/fused-silica-plano-convex-lenses-uncoated-SLSQ-P.html
to do so:
- program a python script that performs a request to the website to retrieve the html (you could use request python module)
- process the html in order to generate a dictionary using the product codes as key, and spec/value pairs as children (see product.json example, and use, for example beautifulsoup for tag extraction)
- save that dictionary to a json file

+ This code performs the required action, but not all the data is present on the webpage
+ So, the non-existent items will be assigned as null to keep homogenity of the data

"""

#import the required libraries: here I use requests and BeautifulSoup as suggested in the task description
from bs4 import BeautifulSoup
import requests
import json
import sys


########################
address = 'https://www.optosigma.com/eu_en/fused-silica-plano-convex-lenses-uncoated-SLSQ-P.html'
#######################

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
    soup.findAll('tr')
    elements = soup.find_all("tr", {"class": "grouped-item"})
except:
    print('BeautifulSoup erred, maybe not installed yet? Terminating...')
    sys.exit()

components = []

# Optosigma webpage is very structured: contains all the data in a single table
#Iterate over all the elements and extract the data
for element in elements:
    try:
        #Find the product specs table
        table = element.findChild('td', {'class': 'grouped-item-spec'}).findChild('table')

        #Extract the data
        item_id = element.findChild('span', {'class': 'sku-cell'}).get_text(strip=True)   
        reference_drawing = element.findChild('td', {'class': 'grouped-item-spec'}).findChild('img')['src']
        diameter = table.findChild('td', {'data-th': 'Diameter φD'}).get_text(strip=True).replace('mm', '').replace('φ', '')
        focal_length = table.findChild('td', {'data-th': 'Focal length f'}).get_text(strip=True).replace('mm', '')
        radius_of_curvature = table.findChild('td', {'data-th': 'Radius of curvature  r'}).get_text(strip=True).replace('mm', '')
        center_thickness = table.findChild('td', {'data-th': 'Center thickness tc'}).get_text(strip=True).replace('mm', '')
        edge_thickness = table.findChild('td', {'data-th': 'Edge thickness te'}).get_text(strip=True).replace('mm', '')
        back_focal_length = table.findChild('td', {'data-th': 'Back focal length fb'}).get_text(strip=True).replace('mm', '')

        lens_shape = element.findChild('td', {'class': 'grouped-item-name'}).findChild('a').get_text(strip=True).split(' Lens')[0]
        if lens_shape == 'Plano Convex':
            lens_shape = 'Plano-Convex'
        else:
            #Here more options can be added for the lens shape
            #this will be sufficient to homogenize the shape data across different vendors
            pass

        design_wavelength = table.findChild('td', {'data-th': 'Design Wavelength'}).get_text(strip=True).replace('nm', ' nm')
        refractive_index = table.findChild('td', {'data-th': 'Refractive index   n<sub>e</sub>'}).get_text(strip=True)
        material = table.findChild('td', {'data-th': 'Material'}).get_text(strip=True)
        ar_coating = table.findChild('td', {'data-th': 'Coating'}).get_text(strip=True)
        clear_aperture = table.findChild('td', {'data-th': 'Clear aperture'}).get_text(strip=True).replace('the diameter', 'Diameter')

        #Some of these parameters are provided in the attached pdf file of the product
        #They can be extracted from the pdf file similarly, but for now we will leave them as nulls
        diopter =  "null"
        reflectance_range = "null"
        surface_flatness = "null"
        spherical_surface_power = "null"
        surface_irregularity = "null"
        damage_threshold = "null"
        abbe_number = "null"
        focal_length_tolerance = "null"
        
        #Form the dict
        item = {
            'optosigma/' + item_id:
            {
                "Back Focal Length (mm)":back_focal_length,
                "Center Thickness (mm)": center_thickness,
                "Damage Threshold": damage_threshold,
                "Diameter (mm)": diameter,
                "Diopter": diopter,
                "Edge Thickness (mm)": edge_thickness,
                "Focal Length (mm)": focal_length,
                "Radius of Curvature (mm)": radius_of_curvature,
                "Reference Drawing": reference_drawing,
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
                
                #extras
                #'Delivery Time': el['data-delivery'],
                #'Price': el['data-price'],
            },
        }
    except:
        #If error -> there may be a network problem or a broken link, just try to fetch the data of the remaining lenses in the list
        print('Component values cannot be found, link may be broken. Item: ' + item_id)
        continue
    
    try:
        #Try to add the dict into the component list
        components.append(item)
    except:
        #If error -> maybe memory overflow? Better terminate
        print('Cannot append to item list, terminating...')
        sys.exit()

try:
    #Try to save the component list in json format
    with open("./Task1/task1.json", "w") as outfile:
        json.dump(components, outfile, ensure_ascii=False)
except:
    #If error -> probably a folder access issue, just terminate for now
    #Can take alternative actions in a future version by checking the cause of the error
    print('Cannot save the file, do you have access to the destination folder?')
    sys.exit()
