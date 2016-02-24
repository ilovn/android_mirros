#!/usr/bin/python
from string import rfind
from time import mktime, strptime
from os import makedirs, path, stat, utime
from urllib import urlretrieve, urlopen
from xml.etree import ElementTree

import urllib2

from sgmllib import SGMLParser
from pyquery import PyQuery as pq
import urllib

base_url = 'https://dl.google.com/'
out_dir = '/data/mirrors'
#out_dir = '/Users/cat'

def download(filename, last_modified):
# print "downlaod:" + filename
   file = out_dir + filename
   print 'Downloading ' + filename
   urlretrieve(base_url + filename, file)
   utime(file, (last_modified, last_modified))

   process(filename)

def process(filename, size=-1):
   file = out_dir + filename
   if path.isfile(file) and stat(file).st_size == size:
      print 'Skipping: ' + filename
      return

   print 'Processing: ' + filename
   handle = urlopen(base_url + filename)
   headers = handle.info()
   content_length = int(headers.getheader('Content-Length'))
   last_modified = mktime(strptime(headers.getheader('Last-Modified'), '%a, %d %b %Y %H:%M:%S %Z'))

   if rfind(filename, '/') > 2:
      dir = out_dir + filename[:rfind(filename, '/')]
   else:
      dir = out_dir

   if not path.isdir(dir):
      print 'Creating ' + dir
      makedirs(dir)

   if not path.isfile(file):
      download(filename, last_modified)
   else:
      file_stat = stat(file)
      if file_stat.st_mtime != last_modified or file_stat.st_size != content_length:
         download(filename, last_modified)
      else:
         print 'Skipping: ' + filename

def fetch(file):
   if base_url in file:
      dir = file[len(base_url) - 1:rfind(file, '/') + 1]
      file = file[rfind(file, '/') + 1:]
   elif 'http' in file:
      return
   else:
      dir = '/'
   process(dir + file)
   base_dir = path.dirname(dir + file)
   if base_dir != '/':
      base_dir += '/'
   print out_dir + dir + file
   # tree = ElementTree.parse(out_dir + dir + file)
   # for element in tree.getiterator():
   #    if element.tag.split('}')[1] == 'url':
   #       if element.text[-4:] != '.xml':
   #          if not 'http' in element.text:
   #             process(base_dir + element.text)
   #       else:
   #          fetch(element.text)
#for file in ['repository-10.xml', 'repository-11.xml', 'addons_list-2.xml']:
   #fetch(file)
#   print file

content = urllib2.urlopen('http://developer.android.com/intl/zh-cn/ndk/downloads/index.html').read()
#print content
d = pq(content)
#print d
#print d.find('a')
#print d('#win-tools').attr('href')
for alinks in d.find('a'):
    #print alinks.text()
    if 'return onDownload(this)' == alinks.get('onclick') or 'return onDownload(this,false,true)' == alinks.get('onclick'):
        print alinks.attrib.get('href')
        fetch(alinks.attrib.get('href').replace('https://dl.google.com/', '').replace('http://dl.google.com/', ''))

