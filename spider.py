import requests

class Spider:
	def __init__(self):
		self.key, self.secret = self.fetch_api_tokens()
    self.url = 'https://api.nytimes.com/svc/archive/v1/2020/1.json?api-key={}'.format(self.key)

  def fetch_api_tokens(self):
    return open('../nyt_api', 'r').readlines()

  def crawl(self, month, year):
    response = requests.get(self.url)
    response = response.json()
    news = response['docs']

    data = []
    # for article in news:
    article = news[0] # let's test with a single one
    res = {
      'headline' : article['headline']['print_headline'],
      'abstract' : article['abstract'],
      'keywords' : list(map(self.keyword, article['keywords']))
    }

  def keyword(self, k):
    return k['value']

  def save_json(self)
    pass
