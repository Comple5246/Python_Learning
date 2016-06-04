# -*- coding:utf-8 -*-
import urllib2
import urllib
import re

#糗事百科爬虫
class QSBK:
	def __init__(self):
		self.baseUrl = 'http://www.qiushibaike.com/hot/page/'
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MISE 5.5; Windows NT)'
		self.headers = {}
		self.headers['User-Agent'] = self.user_agent

		#存放段子，每一个元素为一页的所有段子
		self.stories = []
		#程序运行开关
		self.enable = False

	#根据url获取页面的内容
	def getPage(self, url):
		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageContent = response.read().decode('utf-8')
			return pageContent
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u"连接糗事百科失败：", e.reason
				return None

	def getPageItems(self, pageContent):
		if not pageContent:
			return none
		pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</(.*?)number">(.*?)</',re.S)
		items = re.findall(pattern, pageContent)
		pageStories = []
		for item in items:
			#是否含有图片
			haveImg = re.search('img', item[2])
			if not haveImg:
				replaceBR = re.compile('<br/>')
				text = re.sub(replaceBR, '\n', item[1].strip())
				pageStories.append([item[0].strip(), text, item[3].strip()])
		return pageStories

	def loadPage(self):
		if self.enable == True:
			if len(self.stories) < 2:
				url = self.baseUrl + str(self.pageIndex)
				pageContent = self.getPage(url)
				pageStories = self.getPageItems(pageContent)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex += 1

	def getOneStory(self, pageStories, pageIndex):
		for story in pageStories:
			input = raw_input()
			#判断是否要加载新的页面，如果需要则加载，判断条件在loadPage函数中
			self.loadPage()
			if input == 'Q':
				self.enable = False
				return
			print u'第%d页\t发布人：%s\t赞：%s\n%s' %(pageIndex, story[0], story[2], story[1])


	def start(self):
		print u'正在读取糗事百科段子，按回车查看新段子，Q退出'
		self.enable = True
		self.loadPage()
		nowPage = 0;
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)

if __name__ == '__main__':
	spider = QSBK()
	spider.start()



