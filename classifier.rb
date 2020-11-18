require 'json'

class Classifier
  attr_accessor :year, :dictionary, :months

  def initialize(year)
    @year = year
    @months = (1..12).to_a
    # @months = (1..12).to_a
    @dictionary = JSON.parse(File.read('dictionary.json'))
  end

  def run
    months.each do |month|
      classifications = Hash[(-1..9).to_a.map { |x| [x, []] }]

      news_count = %x(ls "./processed_data/#{year}/#{month}" | wc -l).to_i
      for i in 0..news_count-1
        abstract = JSON.parse(File.read("./processed_data/#{year}/#{month}/#{i}.json"))['abstract']
        abstract.downcase!
        abstract.gsub!(/[^A-Za-z]/, ' ')
        abstract.gsub!(/\s+/, ' ')

        matches = Array.new(10, 0)

        dictionary.each do |key, value|
          key = key.to_i
          value.each do |word|
            matches[key] += 1 if abstract.include?(word)
          end
        end

        max_matches = matches.max

        klass = max_matches.zero? ? -1 : matches.index(max_matches)
        classifications[klass] << i
      end

      File.write("./classifications/#{year}/#{month}.json", JSON.pretty_generate(classifications))
      puts "Finished classifying news from month #{month}"
    end
  end
end

year = 2019
classifier = Classifier.new(year)
classifier.run
