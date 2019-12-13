import os
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import geocoder
from iptcinfo3 import IPTCInfo

# -------------------------- Getting Exif -------------------------------
def get_exif(filename):

    image = Image.open(filename)
    image.verify()

    return image._getexif()

def get_labeled_exif(exif):

    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

# -------------------------- Getting Date -------------------------------

def get_date_exif(filename):

    image = Image.open(filename)
    image.verify()
    raw = image._getexif()[36867]
    processed = raw[0:4] + raw[5:7] + raw[8:10]

    return processed

# -------------------------- Getting Location -------------------------------

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
               if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

# -------------------------- Getting Camera Type -------------------------------

def get_camera_type(filename):
    image = Image.open(filename)
    image.verify()
    camera = image._getexif()[36867]

    return camera

# -------------------------- Getting Keywords -------------------------------

def get_keywords(filename):

    raw_list = IPTCInfo(filename)['keywords']
    list = []
    for words in raw_list:
        keywords = words.decode('utf-8')
        list.append(keywords)

    return list

# -------------------------- Renaming Image -------------------------------

def rename_image(filename):

    list = []

    list.append(get_date_exif(filename))
    list.extend(get_keywords(filename))

    name = '_'.join(list)

    return name

# -------------------------- Testing -------------------------------
print(rename_image('IMG0052.jpg'))
