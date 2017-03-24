#!/usr/bin/ruby

require 'rubygems'
require 'json'
require 'pp'

require 'open3'

cmd ='curl -l -H "Content-Type: application/json" -X GET "https://smart-home-joe.herokuapp.com/washers.json"'

stdout, stderr, status = Open3.capture3(cmd)

obj = JSON.parse(stdout)

puts obj

obj.each do |key, val| 
	puts key
	puts val
end

