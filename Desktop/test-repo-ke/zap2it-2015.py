'''
This script uses zap2it_file.txt file as input.
(Make sure the file contains a list of URL's for TV show profiles pages, 
	for example http://tvschedule.zap2it.com/tv/treehouse-masters/EP01720979?aid=tvschedule).
It then scrapes HTML for the following data points: image source, image url(+partner code), title,
	synopsis, more link(+partner code), episode guide link, and network;
It generates zap2it_out_file.txt text file with all the data and zap2it_out_imhurl_file.txt with image urls'''

import urllib2
import urllib
from bs4 import BeautifulSoup
import codecs
import os

zap2it_file = "zap2it_file.txt"
zap2it_out_file  = "zap2it_out_file.txt"
zap2it_img_out_file  = "zap2it_out_imgurl_file.txt"

def parse_result(url,output,output1):
	url = url.strip()	
	f = urllib2.urlopen(url)
	soup = BeautifulSoup(f)
	
	title = ""
	episode_guide_link_full = ""
	url_full = ""
	img_src_full = ""
	synopsis = ""
	network = ""

	for h1 in soup.find_all('h1',{'id':'zc-program-title'}):
		title=h1.text
		
		if not title:
			title = ''
		
	for li in soup.find_all('li', {'id': 'zc-sc-episodes'}):
		episode_guide_link = li.a['href']
		episode_guide_link_full = episode_guide_link+'?aid=ask'
		
		if not episode_guide_link_full:
			episode_guide_link_full = ''
	
	for img in soup.find_all('img', {'id':'zc-photogal-preview-main-image'}):
		img_src =img['src']
		img_src_full = img_src+'?aid=ask'
		img_src_filename = 'tv/z2/'+img_src.rsplit('/')[-1]
		
		if not img_src_full:
			img_src_full = ''
	
	for p in soup.find_all('p', {'id':'zc-sc-premise'}):
		synopsis_long = p.text
		synopsis = synopsis_long[:synopsis_long.find('.',50)]
		
		if not synopsis:
			synopsis = ''
		
	for	dl in soup.find_all('dl', {'id': 'zc-sc-premiere'}):
		text = dl.text
		network = text[text.find('Network:')+9:-1]
		
		if not network:
			network = ''
	
	url_full = url+'?aid=ask'
		
	result = img_src_filename+'\t'+img_src_full+'\t'+url_full+'\t'+title+'\t'+synopsis+'\t'+url_full+'\t'+episode_guide_link_full+'\t'+network
 	return result
 		
def img_parse_result(url,output,output1):

	url = url.strip()	
	f = urllib2.urlopen(url)
	soup = BeautifulSoup(f)
	
	img_src_full = ""
	
	for img in soup.find_all('img', {'id':'zc-photogal-preview-main-image'}):
		img_src =img['src']
		img_src_full = img_src+'?aid=ask'
		
	if not img_src_full:
		return img_parse_result(url,output,output1)
	else:
		img_result = img_src
		return img_result

def main():
	
	results = []
	img_results = []
	
	input = codecs.open(zap2it_file, 'r','utf8').readlines()
	output = codecs.open(zap2it_out_file,'w+','utf8', 'replace')
 	output1 = codecs.open(zap2it_img_out_file,'w+','utf8','replace')
	
	for url in input:
		result = parse_result(url,output,output1)
		img_result = img_parse_result(url,output,output1)
		results.append(result)
		img_results.append(img_result)
	
 	print results
 	print img_results
 	output.write('\n'.join(results))
 	output1.write('\n'.join(img_results)+'\n')

	input2 = open('zap2it_out_imgurl_file.txt', 'r')

	for line in input2:
  		url = line
		image = url.rsplit('/')[-1]
		image_good = image[:image.find('\n')]
		path = '/Users/sofyamulenok/Desktop/images tv'
		fullpath = os.path.join(path,image_good)
		urllib.urlretrieve(url,fullpath)
 	
if __name__ == "__main__":
	main()