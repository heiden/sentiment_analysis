require 'json'
require 'fileutils'
require 'httparty'

class Spider
  attr_accessor :key, :secret

  def initialize
    @key, @secret = fetch_api_tokens
  end

  def fetch_api_tokens
    credentials = JSON.parse(File.read('../nyt_api'))
    return credentials['key'], credentials['secret']
  end

  def run
    years = (1970..2020).to_a
    months = (1..12).to_a

    years.each do |year|
      months.each do |month|
        crawl(year, month)
        process(year, month)
      end
    end
  end

  def crawl(year, month)
    url = "https://api.nytimes.com/svc/archive/v1/#{year}/#{month}.json?api-key=#{key}"
    response = HTTParty.get(url)
    response = response['response']

    File.write("raw_data/#{year}_#{month}.json", JSON.pretty_generate(response))
  end

  def process(year, month)
    FileUtils.mkdir_p("processed_data/#{year}/#{month}")
    
    file = File.read("raw_data/#{year}_#{month}.json")
    raw_data = JSON.parse(file)
    news = raw_data['docs']

    news.each_with_index do |article, i|
      data = {
        headline: article.dig('headline', 'print_headline'),
        abstract: article.dig('abstract'),
        lead_paragraph: article.dig('lead_paragraph'),
        keywords: article.dig('keywords').map { |keyword| keyword['value'] },
        print_page: article.dig('print_page')
      }

      File.write("processed_data/#{year}/#{month}/#{i}.json", JSON.pretty_generate(data))
    end
  end

  def count_news
    path = './processed_data'
    years = (1970..2020).to_a
    months = (1..12).to_a

    years.each_with_object({}) do |year, buffer|
      buffer[year] = months.map { |month| Dir.glob("#{path}/#{year}/#{month}/*").count }
    end
  end
end

spider = Spider.new
# spider.run
puts spider.count_news
