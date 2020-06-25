from textblob import TextBlob

class Analysis:
	def __init__(self):
		self.key, self.secret = self.fetch_api_tokens()
		self.sentiment = 0
		self.subjectivity = 0
		self.number_of_news = 0

	def run(self): # refactor this method after the spider is finished
		response = requests.get(self.url)
		soup = BeautifulSoup(response.text, 'html.parser')
		# news = soup.find_all('h3', class_ = self.classes)
		self.number_of_news = len(news)
		for headline in news:
			blob = TextBlob(headline.get_text())	
			self.sentiment += blob.sentiment.polarity / self.number_of_news
			self.subjectivity += blob.sentiment.subjectivity / self.number_of_news

analyser = Analysis()
# analyser.run()
# print(analyser.sentiment, analyser.subjectivity)
