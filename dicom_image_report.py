# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 10:26:58 2017

@author: clahn
"""


import gdcm
import re
import sys
import os

# DICOM image file name
filename = "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\Chestxray\\DICOM\\0000F55C\\AA7ADF64\\AA4C57E5\\000005DC\\EEC0B8EC"
#Chest  "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\Chestxray\\DICOM\\0000F55C\\AA7ADF64\\AA4C57E5\\000005DC\\EEC0B8EC"
#Hand   "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\wrist\\DICOM\\00004F50\\AAB6729B\\AADF669E\\0000BD75\\EE48ACFC"
#lspine   "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\lspine\\DICOM\\00003854\\AA0906AD\\AAAC10C7\\0000D8BE\\EEB903E6"
#CT Topogram   "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\Chestxray\\DICOM\\0000F55C\\AA7ADF64\\AA4C57E5\\000074FF\\EE456165"
#GE pelvis  "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\GE Pelvis\\DICOM\\0000A70B\\AAC000DE\\AA3DE55F\\0000EB0B\\EE3AEF33"
#konica DR chest "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\konica chest\\DICOM\\000073F7\\AA0CE04D\\AACFF714\\0000F835\\EED617E4"
#carestream CR cspine  "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\carestream cr cspine\\DICOM\\00001238\\AADF1C2D\\AA85AD74\\0000E397\\EEEE731F"
#carestream dr lateral cspine "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\carestream dr cspine\\DICOM\\0000C4EE\\AAE4FDE2\\AABDE4A4\\00005D8F\\EEBA03FB"
#philips CR chest  "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\philips cr chest\\DICOM\\0000AF3C\\AAB4B1E3\\AA74219B\\00001D31\\EEB65815"
#Konica CR  "W:\\SHARE8 Physics\\Software\\python\\scripts\\clahn\\pythontestimages\\ankle konica cr\\DICOM\\0000ADF4\\AAE01A21\\AA3EA8FA\\0000F25E\\EE0B6167"

# Instanciate a gdcm.Reader
# This is the main class to handle any type of DICOM object
# You should check for gdcm.ImageReader for reading specifically DICOM Image file
r = gdcm.Reader()
r.SetFileName( filename )

# If the reader fails to read the file, we should stop !
if not r.Read():
    print ("Not a valid DICOM file")

 # Get the DICOM File structure
file = r.GetFile()

# Get the DataSet part of the file
dataset = file.GetDataSet()

# Ok let's print it !
#print dataset

# Use StringFilter to print a particular Tag:
sf = gdcm.StringFilter()
sf.SetFile(r.GetFile())

# Check if Attribute exist
#print dataset.FindDataElement(gdcm.Tag(0x0008, 0x2218))

 # Let's print it as string pair:
#print sf.ToStringPair(gdcm.Tag(0x18, 0x1110))[1]
#prints just the value for this dicom element
#print sf.ToStringPair(gdcm.Tag(0x28, 0x0030))[1]

#this is just a function to test getting the user inputted acc# to query the database.
#TODO: This function will be rewrittent to get the dicom header from the database using the
#user inputted accession number.


#prints accession # inputed by user in pyqt_text_gui.py
print ("Exam Accession #" + sys.argv[1])
print ()


#separate out site info in output text
print ("SITE INFO:")

#this prints the station name
def get_station_name():
    statest = dataset.FindDataElement(gdcm.Tag(0x0008, 0x1010))
    sta = sf.ToStringPair(gdcm.Tag(0x0008, 0x1010))[1]

    if statest == True:
        print ("The station name is " + str(sta).strip())
    else:
        print ("Station name is not available for this exam.")

get_station_name()


#this prints the equipment type
def get_equipment_name():
    equiptest = dataset.FindDataElement(gdcm.Tag(0x0008, 0x1090))

    if equiptest == True:
        equip = sf.ToStringPair(gdcm.Tag(0x0008, 0x1090))[1]
        vendor = str.lower(sf.ToStringPair(gdcm.Tag(0x0008, 0x0070))[1]).strip()
        print ("The vendor name is " + str(vendor).strip())
        print ("The equipment name is " + str(equip).strip())
    else:
        print ("Equipment name is not available for this exam.")

get_equipment_name()


#This checks what type of detector was used and prints the type listed in DICOM info.
def check_detector():
    detchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x7004))
    det = sf.ToStringPair(gdcm.Tag(0x0018,0x7004))[1]

    if detchk == True:
        print ("The detector type used for this exam was" +  '"' + det.lower().strip() + '".')

    else:
        print ("There is not any detector information available for this exam.")

check_detector()


#this prints the site name (if avalaible)
def get_site_name():
    sitetest = dataset.FindDataElement(gdcm.Tag(0x0008, 0x0080))
    site = sf.ToStringPair(gdcm.Tag(0x0008, 0x0080))[1]

    if sitetest == True:
        if site.strip() == '':
            print ("Site name is not available for this exam.")
        else:
            print ("The site name is " + str(site).strip())
    else:
        print ("Site name is not available for this exam.")

get_site_name()


#this prints the site address (if avalaible)
def get_site_address():
    addtest = dataset.FindDataElement(gdcm.Tag(0x0008, 0x0081))
    add = sf.ToStringPair(gdcm.Tag(0x0008, 0x0081))[1]

    if addtest == True:
        print ("The address is " + str(add).lower().strip)
    else:
        print ("Site address is not available for this exam.")

get_site_address()

#print blank line
print ("")

#sepearate out exam info in output text
print ("EXAM INFO:")

def get_exam_name():
    #  exam = sf.ToStringPair(gdcm.Tag(0x08, 0x104))[1]
    #  can't figure out how to get nested tag value for exam
    #  print str.upper(exam) + " is the exam type."
    if dataset.FindDataElement(gdcm.Tag(0x08, 0x103e)) == True:
        view = sf.ToStringPair(gdcm.Tag(0x08, 0x103e))[1]
        part = sf.ToStringPair(gdcm.Tag(0x18, 0x15))[1]
        study = sf.ToStringPair(gdcm.Tag(0x008, 0x1030))[1]
        print (study)
        print (part.upper().strip() + " is the bodypart type for this exam.")
        print (view.upper().strip() + " is the view.")
    else:
        print ("Exam part data not available for this exam.")

get_exam_name()


#print blank line
print ("")

#separte out sid in output text
print ("SID INFO:")

#This assesses if SID is appropriate for exam
def sid_check():
    sid = float(sf.ToStringPair(gdcm.Tag(0x18, 0x1110))[1])
    part = sf.ToStringPair(gdcm.Tag(0x18, 0x15))[1]
    view = sf.ToStringPair(gdcm.Tag(0x08, 0x103e))[1]
    study = sf.ToStringPair(gdcm.Tag(0x008, 0x1030))[1]
    sidconv = sid * 0.0393

    if sid == 0 or sid == '':
        print ("SID is not available on this exam.")
    elif part.lower().strip() == "chest":
        if sid <= 1800:
            print ("The SID used was %.2f inches.\n"
                  "This SID is less than recommended for this exam." % (sidconv))
        else:
            print ("The SID used was %.2f inches.\n"
                  "This SID is appropriate for this exam." % (sidconv))
    elif "cervical" in study.lower().strip() and view.lower().strip() == "lateral":
        if sid <= 1800:
            print ("The SID used was %.2f inches.\n"
                  "This SID is less than recommended for this exam." % (sidconv))
        else:
            print ("The SID used was %.2f inches.\n"
                  "This SID is appropriate for this exam." % (sidconv))
    else:
        if sid <= 1000 or sid >= 1250:
            print ("The SID used was %.2f inches.\n"
                  "This SID is not the recommended distance for this exam." % (sidconv))
        else:
            print ("The SID used was %.2f inches.\n"
                  "This SID is appropriate for this exam." % (sidconv))


#check to see if sid is available
def sid_checker():
    sidtest = dataset.FindDataElement(gdcm.Tag(0x0018, 0x1110))

    if sidtest == True:
         sid_check()
    else:
        print ("SID information is not available for this exam.")
        pass

sid_checker()


#print blank line
print ("")

#separate out exposure info in output text
print ("EXPOSURE INFO:")


#need to add CR EI/IEC scale values?  base off modality CR or DX (0x0008, 0x0060)
#Dictionary based exposure index check for iec. Need to add more vendor EI values to the dictionary.
def drexposure_check():
    exptest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1411))

    if exptest == True:
        expiec = sf.ToStringPair(gdcm.Tag(0x18,0x1411))[1]
        eifloat = float(expiec)
        vendor = str.lower(sf.ToStringPair(gdcm.Tag(0x0008, 0x0070))[1]).strip()
        exp_dict = {'kodak':[100, 220], 'ge healthcare': [125,500], 'konica minolta':[100,300]}

        for name, ei in iter(exp_dict.items()):
            if name == vendor:
                if eifloat >= ei[1]:
                    print (
                            "Vendor is " + vendor.lower().strip() +
                            ".  IEC is " + str(float(expiec)).lower().strip() +
                            ". Exceeds recommended targets."
                            )
                elif eifloat <= ei[0]:
                    print (
                            "Vendor is " + vendor.lower().strip() +
                            ".  IEC is " + str(float(expiec)).lower().strip() +
                            ".  Exposure is below recommended targets."
                            )
                else:
                    print (
                            "IEC is " + str(float(expiec)).lower().strip() +
                            ".  This is within recommended targets."
                            )
    else:
        print ("There is no exposure data available for this exam.")


#TODO:  Update CR exposure nubmers to appropriate index for iec.
#Dictionary based exposure index check for iec. Might not work for CR since each vendor uses a proprietary index with different DICOM values.
def crexposure_check():
    exptest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1411))

    if exptest == True:
        expiec = sf.ToStringPair(gdcm.Tag(0x18,0x1411))[1]
        eifloat = float(expiec)
        vendor = str.lower(sf.ToStringPair(gdcm.Tag(0x0008, 0x0070))[1]).strip()
        exp_dict = {'kodak':[100, 220], 'ge healthcare': [125,500], 'konica minolta':[100,300]}

        for name, ei in iter(exp_dict.items()):
            if name == vendor:
                if eifloat >= ei[1]:
                    print (
                            "Vendor is " + vendor.lower().strip() +
                            ".  IEC is " + str(float(expiec)).lower().strip() +
                            ". Exceeds recommended targets."
                            )
                elif eifloat <= ei[0]:
                    print (
                            "Vendor is " + vendor.lower().strip() +
                            ".  IEC is " + str(float(expiec)).lower().strip() +
                            ".  Exposure is below recommended targets."
                            )
                else:
                    print ("IEC is " + str(float(expiec)).lower().strip() +
                           ".  This is within recommended targets."
                           )
    else:
        print ("There is no IEC exposure data available for this exam.")


#this checks if the exam was done on cr or dr.  It prints the cr exposure index (carestream and philips)
#or calls the dr or cr (konica only) exposure index check dictionary for iec.
def modality_check():
    modalitytest = dataset.FindDataElement(gdcm.Tag(0x0008, 0x0060))
    modality = sf.ToStringPair(gdcm.Tag(0x0008, 0x0060))[1]
    vendor = str.lower(sf.ToStringPair(gdcm.Tag(0x0008, 0x0070))[1]).strip()
    exp = str.lower(sf.ToStringPair(gdcm.Tag(0x0018, 0x1405))[1]).strip()
    expph = str.lower(sf.ToStringPair(gdcm.Tag(0x0018, 0x6000))[1]).strip()
    ti = str.lower(sf.ToStringPair(gdcm.Tag(0x0018, 0x1412))[1]).strip()
    di = str.lower(sf.ToStringPair(gdcm.Tag(0x0018, 0x1413))[1]).strip()
    strmodality = str(modality).lower().strip()
    print ("The modality type is", strmodality)

    if modalitytest == True:
        if strmodality == "cr" and vendor == "kodak":
            print ("IEC is not available for this exam.\n"
                  "The Carestream Exposure Index for this exam is", exp)
        elif strmodality == "cr" and vendor == "philips medical systems":
            print ("IEC is not available for this exam.\n"
                  "The Philips S number for this exam is", expph)
        elif strmodality == "cr" and vendor == "konica minolta":
            crexposure_check()
            print ("The Konica S number for this exam is", expph)
        elif strmodality == "dx" and vendor == "kodak":
            drexposure_check()
            print ("The Carestream Exposure Index for this exam is", exp)
        elif strmodality == "dx" and vendor == "konica minolta":
            drexposure_check()
            print ("The Konica S Number Exposure Index for this exam is", expph)
        elif strmodality == "dx" and vendor == "ge healthcare":
            drexposure_check()
            print ("The GE Exposure Index for this exam is", exp)
    else:
        print ("Modality not available")
    print ("The Target Index for this exam is", float(ti))
    print ("The Deviation Index for this exam is", float(di))

modality_check()

'''
This was my oringinal way of doing an exposure check with a separate function for each vendor.  Now using dictionary based method.


#This checks to see if IEC is within Carestream 100-220 range for DR
def carestream_exposure_check():
    exptest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1411))
    exp = sf.ToStringPair(gdcm.Tag(0x18,0x1411))[1]

    if exptest == True:
        if float(exp) >= 220.0:
            print "Exposure is " + exp.lower().strip() + ". Exceeds recommended targets."
        elif float(exp) <= 100.0:
            print "Exposure is " + exp.lower().strip() + ".  Exposure is below recommended targets."
        else:
            print "Exposure is " + exp.lower().strip() + ".  This is within recommended targets."
    else:
        print "There is no exposure data available for this exam."


 #This checks to see if IEC is within GE 200-600 range for DR
def ge_exposure_check():
    exptest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1411))
    exp = sf.ToStringPair(gdcm.Tag(0x18,0x1411))[1]

    if exptest == True:
        if float(exp) >= 500.0:
            print "Exposure is " + exp.lower().strip() + ". Exceeds recommended targets."
        elif float(exp) <= 125.0:
            print "Exposure is " + exp.lower().strip() + ".  Exposure is below recommended targets."
        else:
            print "Exposure is " + exp.lower().strip() + ".  This is within recommended targets."
    else:
        print "There is no exposure data available for this exam."


# This chooses which exposure scale to use
def choose_exposure_check():
    vendor = str.lower(sf.ToStringPair(gdcm.Tag(0x0008, 0x0070))[1]).strip()
    if vendor == "ge healthcare":
        ge_exposure_check()
    elif vendor == "kodak":
        carestream_exposure_check()

choose_exposure_check()

'''

print ()
print ("TECHNIQE INFO:")

#check for kV info and print the result
def check_kv():
    kvchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x0060))

    if kvchk == True:
        kv = sf.ToStringPair(gdcm.Tag(0x0018,0x0060))[1]
        print ("The kV used for this exam was", kv)
    else:
        print ("There is not any kV information available for this exam.")

check_kv()


#check for mAs info and print the result
def check_mas():
    maschk = dataset.FindDataElement( gdcm.Tag(0x0018,0x1153))

    if maschk == True:
        masu = sf.ToStringPair(gdcm.Tag(0x0018,0x1153))[1]
        mas = int(masu) * .001
        print ("The mAs used for this exam was", mas)
    else:
        print ("There is not any mAs information available for this exam.")

check_mas()


#This checks if AEC was used and prints the mode listed in DICOM info.
def check_aec():
    aecchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x7060))
    aec = sf.ToStringPair(gdcm.Tag(0x0018,0x7060))[1]
    aecmode = sf.ToStringPair(gdcm.Tag(0x0018,0x7062))[1]

    if aecchk == True:
        print ("Automatic Exposure Control was used for this exam.\n"
              "The AEC setting used was" +  '"' + aec.lower().strip() + '".')
        print ("The AEC mode used was" + ' "' + aecmode.lower().strip() + '".')
    else:
        print ("There is not any AEC information available for this exam.")

check_aec()


def check_filtration():
    ftchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x7050))


    if ftchk == True:
        ftmat = sf.ToStringPair(gdcm.Tag(0x0018,0x7050))[1]
        ftmax = sf.ToStringPair(gdcm.Tag(0x0018,0x7054))[1]
        ftmin = sf.ToStringPair(gdcm.Tag(0x0018,0x7052))[1]
        print (
                "The filter used for this exam was " + ftmat.lower().strip() +
                ". \nFilter minimum thickness of " + ftmin.lower().strip() +
                " and a max thickness of " + ftmax
                )
    else:
        print (
                "A filter was not used for this exam", \
               "or filter information is not available on this unit."
               )

check_filtration()


#print blank line
print ("")

#separate out collimation info in output text
print ("COLLIMATION INFO:")


#This prints the distance of collimation/masking coverted from pixels to mm and inches
def pixel_to_distance():
    pixdistest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1164))
    pixdis = sf.ToStringPair(gdcm.Tag(0x18, 0x1164))[1]
    pixdis2 = float(pixdis[0:5]) #this grabs the first value of two that pixdis returns
    collt = float(sf.ToStringPair(gdcm.Tag(0x18, 0x1702))[1])
    colrt = float(sf.ToStringPair(gdcm.Tag(0x18, 0x1704))[1])
    coltop = float(sf.ToStringPair(gdcm.Tag(0x18, 0x1706))[1])
    colbtm = float(sf.ToStringPair(gdcm.Tag(0x18, 0x1708))[1])
    horiz = (colbtm - coltop) * pixdis2
    vert =  (colrt - collt) * pixdis2
    horizinch = horiz * 0.0393
    vertinch = vert * 0.0393

    if pixdistest == True:
        print (
                "The horizontal collimation (or masking) distance is %4.1fmm. %2.2f in inches." % (horiz, horizinch)
               )
        print (
                "The vertical collimation (or masking) distance is %4.1fmm. %2.2f in inches." % (vert, vertinch)
                )
    else:
        print ("There is no collimation data available for this exam.")


#This prints the distance of collimation/masking coverted from pixels to mm and inches.  Works on polygon collimator shape only.
def imagerpixel_to_distance():
    #This builds a list of collimation vertices from the tuple that is in the DICOM info.  Used with imagerpixel_to_distance
    col = sf.ToStringPair(gdcm.Tag(0x18, 0x1720))[1]
    collist = []
    for i in col.split("\\"):
         collist.append(i)

    pixdistest = dataset.FindDataElement(gdcm.Tag(0x18, 0x1164))
    pixdis = sf.ToStringPair(gdcm.Tag(0x18, 0x1164))[1]
    pixdis2 = float(pixdis[0:5]) #this grabs the first value of two that pixdis returns
    collowrtx = float(collist[0])
    collowltx = float(collist[2])
    coltoplty = float(collist[5])
    colbtmlty = float(collist[1])
    horiz = (collowrtx - collowltx) * pixdis2
    vert = (colbtmlty - coltoplty) * pixdis2
    horizinch = horiz * 0.0393
    vertinch = vert * 0.0393

    if pixdistest == True:
        print (
                "The horizontal collimation (or masking) distance is %4.1fmm. %2.2f in inches." % (horiz, horizinch)
                )
        print (
                "The vertical collimation (or masking) distance is %4.1fmm. %2.2f in inches." % (vert, vertinch)
                )
    else:
        print ("There is no collimation data available for this exam.")


 #This function looks for the collimator shpae in DICOM and calls appropriate collimation distance function.
def choose_collimation():
    coltype = str.lower(sf.ToStringPair(gdcm.Tag(0x18, 0x1700))[1]).strip()
    if coltype == "polygonal":
        imagerpixel_to_distance()
    elif coltype == "rectangular":
        pixel_to_distance()
    else:
        print ("Colimation information is not available for this exam.")

choose_collimation()


def exposed_area():
    ftchk = dataset.FindDataElement( gdcm.Tag(0x0040,0x0303))

    if ftchk == True:
        area = sf.ToStringPair(gdcm.Tag(0x0040,0x0303))[1]
        widtharea = re.findall(r'\d+', area)[0]
        hieghtharea = re.findall(r'\d+', area)[1]
        colwinch = float(widtharea) * 0.393
        colhinch = float(hieghtharea) * 0.393
        print (
                "The exposed area width is %.1f cm and %.2f inches." % (float(widtharea), float(colwinch))
               )
        print (
                "The exposed area hieght is %.1f cm and %.2f inches." % (float(hieghtharea), float(colhinch))
                )
    else:
        print ("There is no exposure area data available for this exam.")

exposed_area()


print ("")

print ("MISC. INFO:")

#This checks if a grid was used and prints the type listed in DICOM info.
def check_grid():
    gridchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x1166))
    grid = sf.ToStringPair(gdcm.Tag(0x0018,0x1166))[1]


    if gridchk == True:
        print (
                "The grid type used for this exam was" +
                '"' + grid.lower().strip() + '".'
                )

    else:
        print ("There is not any grid information available for this exam.")

check_grid()


#This checks if a grid was used and prints the type listed in DICOM info.
def check_algorithm():
    alchk = dataset.FindDataElement( gdcm.Tag(0x0018,0x1400))
    al = sf.ToStringPair(gdcm.Tag(0x0018,0x1400))[1]

    if alchk == True:
        print ("The processing algorithm used for this exam was" +
               '"' + al.lower().strip() + '".'
               )

    else:
        print (
                "There is not any processing algorithm", \
                "information available for this exam."
                )

check_algorithm()


print ("")
print ("-----")
print ("")

