require 'json'

class Parser
  attr_accessor :year

  def initialize(year)
    @year = year
  end

  def list_files
    # Dir.glob('./processed_data/*/*/*')
    Dir.glob("./processed_data/#{year}/*/*")
  end

  def parse
    puts "Starting year #{year}"

    # files = list_files

    # @abstracts = files[0..10].map do |file|
    #   json = File.read(file)
    #   data = JSON.parse(json)
    #   abstract = data['abstract'].to_s # sanitize, could be nil
    # end

    @abstracts = File.open("./parsed_data/parsed_#{year}.data").readlines.map(&:chomp)

    @abstracts.compact!

    lower_sentences
    puts "[#{@abstracts.count} abstracts] Finished lowering sentences"

    remove_digits_and_special_characters
    puts "[#{@abstracts.count} abstracts] Finished removing digits and special characters"

    remove_extra_spaces
    puts "[#{@abstracts.count} abstracts] Finished removing extra spaces"
    
    File.open("parsed_#{year}.data", 'a') { |output| @abstracts.each { |abstract| output.puts(abstract) } }
    puts "[#{@abstracts.count} abstracts] Finished parsing"
    puts "\n"
  end

  def lower_sentences
    @abstracts.map!(&:downcase).compact!
  end

  def remove_digits_and_special_characters
    @abstracts.map! { |abstract| abstract.gsub!(/[^A-Za-z]/, ' ') }.compact!
  end

  def remove_extra_spaces
    @abstracts.map! { |abstract| abstract.gsub(/\s+/, ' ') }.compact!
  end
end

years = (2000..2020).to_a

years.each do |year|
  parser = Parser.new(year)
  parser.parse
end
