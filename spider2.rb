require 'json'
require 'fileutils'
require 'httparty'

# maps a stock string name to the corresponding ticker
TICKERS = {
  'apple' => 'AAPL',
  'microsoft' => 'MSFT',
  'amazon' => 'AMZN',
  'google' => 'GOOG',
  'facebook' => 'FB',
  'berkshire hathaway' => 'BRK-B',
  'visa' => 'V',
  'walmart' => 'WMT',
  'johnson & johnson' => 'JNJ',
  'procter & gamble' => 'PG'
}

class Spider
  attr_accessor :key, :stock, :year

  def initialize(stock, year)
    @key = fetch_api_tokens
    @stock = stock
    @year = year

    FileUtils.mkdir_p("data_from_queries/#{year}")
  end

  def fetch_api_tokens
    credentials = JSON.parse(File.read('../nyt_api'))
    return credentials['key2']
  end

  def extract_page
    log = File.readlines("./data_from_queries/control.csv")
    log.map!(&:chomp)

    pairs = log.each_with_object({}) do |pair, acc| 
      k, v = pair.split(';')
      acc[k] = v
    end

    pairs[stock].to_i
  end

  def crawl(page = 0)
    file = File.open("./data_from_queries/#{year}/#{TICKERS[stock]}.csv", 'a')

    file.write('Headline;Month;Day') if page == 0 # csv header

    while true do
      success = false
      
      query = {
        'q': stock,
        # 'fq': 'news_desk:("Finances")',
        'facet_field': 'day_of_week',
        'facet': 'true',
        'begin_date': "#{year}0101",
        'end_date': "#{year}1231",
        'page': (page += 1).to_s,
        'api-key': key
      }

      # query = {'q': 'apple', 'facet_field': 'day_of_week', 'facet': 'true', 'begin_date': "20200101", 'end_date': "20201231", 'page': '44', 'api-key': 'vyU2rqsZASN6z3Fe1FUSB6CXqEe9EmES'}

      url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?#{URI.encode_www_form(query)}"

      response = HTTParty.get(url)

      # while response.code != 200
      #   puts("sleepin' for 5 secs before retrying"), sleep(5)
      #   response = HTTParty.get(url)
      # end

      puts "#{stock}, page #{page}: code #{response.code}"

      if response.code != 200 || page == 50
        control = File.open('./data_from_queries/control.csv', 'a')
        control.write("#{stock};#{page - 1}\n")
        control.close
        file.close
        return
      end
      
      documents = response['response']['docs']

      # puts response['docs'].map { |doc| doc['headline']['main'] }
      documents.each do |doc|
        date = Date.parse(doc['pub_date'])
        file.write("#{doc['headline']['main'].gsub(';', ',')};#{date.month};#{date.day}\n")
      end

      sleep(15) if page % 10 == 0 # I think my requests are being blocked at some point... :thinking:
      sleep(1)
    end
  end
end

year = 2019
stocks = File.readlines("./data_from_queries/stocks")
stocks.map!(&:chomp)

stocks.each do |stock|
  spider = Spider.new(stock, year)
  starting_page = spider.extract_page || 0
  spider.crawl(starting_page)
  sleep(60)
end
