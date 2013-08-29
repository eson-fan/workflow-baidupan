#encoding:utf8

import urllib,urllib2
import re
from xml.etree import ElementTree

# author: eson fan
# email: esonfan@gmail.com
# date: 2013-08-25

url = 'http://www.baidu.com/s?'
site = r" site:pan.baidu.com"

def __searchBDPan(keyword):
	listItem = []
	if keyword:
		keyword = keyword + site
		param = {
			'ie':'utf-8',
			'wd':keyword,
			'inputT':'0'
		}
		try:
			f = urllib2.urlopen(url + urllib.urlencode(param))
			content = f.read()
			f.close()

			reg = r'<table class=\"result\" id=\"\d\"[\s|\S]+?</span></div></td></tr></table>'
			tableContent = re.findall(reg, content, re.S)

			# regLink = re.compile(r'<h3 class=\"t\".*<a.*href=\"http:\/\/www.baidu.com\/link\?url=(.*?)\".*?>(.*)</a></h3>', re.S) #匹配 
			regLink = re.compile(r'<h3 class=\"t\".*<a.*href=\"(.*?)\".*?>(.*)</a></h3>', re.S) #匹配 
			for l in tableContent:
				m = regLink.search(l)
				#注：这里需要讲读取出来的字符串接码为unicode编码，然后到输出的时候按需要编码
				listItem.append(BDPanItem(m.group(2).replace('<em>', '《').replace('</em>', '》').decode('utf-8'), m.group(1).decode('utf-8')))
		except Exception, e:
			pass
		
	return listItem

def __toFeedbackXML(list):
	rootElement = ElementTree.Element("items")
	if list:
		for l in list:
			__addItem(rootElement, l.name, l.link, 'yes')
	else:
		__addItem(rootElement, '未搜索到内容，请重新搜索...', '', 'no')
	return ElementTree.tostring(rootElement, 'utf-8') #按需要编码

def __addItem(parent,title,arg = None,valid = 'yes'):
	item = ElementTree.SubElement(parent, "item")
	if arg:
		item.set('arg', arg)
	item.set('valid', valid)
	titleItem = ElementTree.SubElement(item, 'title')
	titleItem.text = title
	subtitle = ElementTree.SubElement(item, 'subtitle')
	subtitle.text = u'回车(或点击)在浏览器打开选中资源，按alt+回车(或点击)赋值链接到粘贴板..'
	iconItem = ElementTree.SubElement(item, 'icon')
	iconItem.text = 'icon.png'

def search(keyword):
	return __toFeedbackXML(__searchBDPan(keyword));

class BDPanItem:
	'''百度盘抓取到的内容'''

	def __init__(self,name,link):
		self.name = name
		self.link = link

	def __str__(self):
		return self.name + "--->" + self.link

class SearchException(BaseException):
	'''搜索异常'''
	def __init__(self, msg):
		self.msg = msg


if __name__ == '__main__':
	print search('侦探')