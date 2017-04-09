#!/usr/bin/ruby

require 'rubygems'
require 'json'
require 'pp'

require 'open3'

cmd ='curl -l -H "Content-Type: application/json" -X GET "https://smart-home-joe.herokuapp.com/washers.json"'

stdout, stderr, status = Open3.capture3(cmd)

obj = JSON.parse(stdout)

obj[0].each do |key, val| 
	puts key
	puts val
	if key == "start_stop"
		if val == "start"
			# check the timestamp of this schedule
		end
	end
end

