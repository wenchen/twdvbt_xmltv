#!/usr/bin/env python
#coding:utf-8

import sys, json, urllib, datetime, subprocess
import xml.etree.cElementTree as ET
from xml.dom import minidom
from pprint import pprint
import re

def fixDefaultEncoding():
    # sys.setdefaultencoding() does not exist, here!
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')

def loadChannel():
    with open('data.json') as json_file:
        data=json_file.read()
    return json.loads(data)

def loadGuideFromWeb(data):
    prog = re.compile('(.+)\(([0-9]*)\)$')
    for _, channel in enumerate(data):
        url = channel['GuideURL']
        guide_data = json.loads(urllib.urlopen(url).read())['list']
        guides = []
        guide_data.sort(key=lambda x: x["key"])
        for day_guide in guide_data:
            guides = guides + day_guide['values']

        for i, guide in enumerate(guides):
            if len(guides) == i+1:
                break;
            gd = {}
            if "（重）" in guide['name']:
                guide['name'] = guide['name'].replace("（重）","")
            pTitle = prog.match(guide['name'])
            if pTitle is None:
                gd["Title"] = guide['name']
            else:
                gd["Title"] = pTitle.group(1)
                gd["EpisodeNumber"] = pTitle.group(2)
            gd["StartTime"] = guide['date'].replace("-","")+guide['time'].replace(":","")+"00 +0800"
            gd["EndTime"] = guides[i+1]['date'].replace("-","")+guides[i+1]['time'].replace(":","")+"00 +0800"
            channel['Guide'].append(gd)

    return data
    
def generatXMLTV(data):
    timezone_offset = subprocess.check_output(['date', '+%z']).strip()
    xml = ET.Element("tv")
    for channel in data:
        xmlChannel = ET.SubElement(xml, "channel", id=channel['GuideName'])
        ET.SubElement(xmlChannel, "display-name").text = channel['GuideName'] 
        ET.SubElement(xmlChannel, "display-name").text = channel['GuideNumber']
        if 'Affiliate' in channel:
            ET.SubElement(xmlChannel, "display-name").text = channel['Affiliate']
        if 'ImageURL' in channel:
            ET.SubElement(xmlChannel, "icon", src=channel['ImageURL'])
        if 'URL' in channel:
            ET.SubElement(xmlChannel, "url").text = channel['URL']
        for program in channel["Guide"]:
            xmlProgram = ET.SubElement(xml, "programme", channel=channel['GuideName'])
            xmlProgram.set("start", program['StartTime'])
            xmlProgram.set("stop", program['EndTime'])
            ET.SubElement(xmlProgram, "title").text = program['Title']
            if 'EpisodeNumber' in program:
                ET.SubElement(xmlProgram, "episode-num").text = program['EpisodeNumber']
            if 'EpisodeTitle' in program:
                ET.SubElement(xmlProgram, "sub-title").text = program['EpisodeTitle']
            if 'Synopsis' in program:
                ET.SubElement(xmlProgram, "desc").text = program['Synopsis']
            if 'OriginalAirdate' in program:
                ET.SubElement(xmlProgram, "date").text = datetime.datetime.fromtimestamp(program['OriginalAirdate']).strftime('%Y%m%d%H%M%S') + " " + timezone_offset
            if 'PosterURL' in program:
                ET.SubElement(xmlProgram, "icon", src=program['PosterURL'])
            if 'Filter' in program:
                for filter in program['Filter']:
                    ET.SubElement(xmlProgram, "category").text = filter
    reformed_xml = minidom.parseString(ET.tostring(xml).encode('utf-8'))
    return reformed_xml.toprettyxml(encoding='utf-8')
                    
def saveStringToFile(strData, filename):
    with open(filename, 'w') as outfile:
        outfile.write(strData)
                    
def loadJsonFromFile(filename):
    return json.load(open(filename))

def saveJsonToFile(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)
                    
def main():
    fixDefaultEncoding()
    data = loadChannel()
    data = loadGuideFromWeb(data)    
    xmltv = generatXMLTV(data)
    saveStringToFile(xmltv, "output/hdhomerun.xml")

  
if __name__== "__main__":
  main()
