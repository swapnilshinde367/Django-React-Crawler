import re
import bs4
import requests
from urllib.parse import urlparse
from rest_framework.views import APIView
from . serializers import CrawlerSerialzer
from rest_framework.response import Response

import sys

class Crawler( APIView ) :

	def get( self, request ) :

		strUrl = request.GET.get('url').strip('/')
		intDepth = int(request.GET.get('depth'))

		strParsedURI = urlparse( strUrl )
		strDomain = '{uri.netloc}'.format( uri = strParsedURI )

		intCount = 0
		lststrLinks = []

		strHtml = self.handleGetHtml(strUrl)
		if None != strHtml :
			for strLink in strHtml.find_all( 'a', recursive = True ) :
				if intCount >= intDepth :
					break
				strHref = strLink.get('href')
				if strHref != None \
					and strDomain in strHref \
					and strUrl != strHref.strip('/') \
					and 'mailto' not in strHref:

					if False == bool(urlparse(strHref).scheme) :
						strHref = urlparse(strHref)._replace(**{"scheme": "http"})
						lststrLinks.append( strHref.geturl() )
					else :
						lststrLinks.append( strHref )

					intCount = intCount + 1

			lststrResponse = []

			intCount = 1
			for strLink in lststrLinks :
				lststrImages = []
				strHtml = self.handleGetHtml(strLink)
				for strImage in strHtml.find_all( 'img',{"src":True}, recursive = True ) :
					strSrc = strImage['src']
					if strSrc != None:
						if False == bool(urlparse(strSrc).scheme) :
							strSrc = urlparse(strSrc)._replace(**{"scheme": "http"})
							lststrImages.append( strSrc.geturl() )
						else :
							lststrImages.append(strSrc)

				lststrResponse.append( { 'id': intCount,'url': strLink, 'images' : lststrImages } )
				intCount = intCount + 1

			objResults = CrawlerSerialzer(lststrResponse, many=True).data
			return Response( objResults )
		else :
			objResults = CrawlerSerialzer( { 'id' : 0, 'url': '', 'images' : [] }).data
			return Response( objResults )

	def handleGetHtml( self, strUrl ) :
		try :
			objResponse = requests.get(strUrl)
			strHtml = objResponse.text
			strHtml = bs4.BeautifulSoup( objResponse.text, 'html.parser' )
			return strHtml
		except :
			return None
