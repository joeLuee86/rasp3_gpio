#!/usr/bin/ruby

require 'rubygems'
require 'json'
require 'pp'
require 'time'

require 'open3'

REST_CMD ='curl -l -H "Content-Type: application/json" -X GET "https://smart-home-joe.herokuapp.com/washers.json"'
TIME_STAMP = "08:00:00"
puts Time.parse(TIME_STAMP)

time_out = false
cur_channel = "null"

while true do 
	# query server for commands periodically
	stdout, stderr, status = Open3.capture3(REST_CMD)
	obj = JSON.parse(stdout)
	puts obj

	obj[0].each do |key, val| 

		if key == "channel"
			cur_channel = val 
		end

		if key == "start_at"
			dest_time = Time.parse(TIME_STAMP)
			set_time = Time.parse(val)
			if dest_time < set_time
				# it's time to wash now
				time_out = true
				puts "it's time to wash now"
			end
		end

		if key == "start_stop"
			# if val == "start"
			if true
				if time_out
					# now start washing
					puts "now, start washing"
					wash_cmd = "blink_gpio.py " +  cur_channel + " start"
					puts wash_cmd
					system(wash_cmd)
				end				
			end
		end
	end

	sleep(10)
	puts "after 10s sleep"

	# check humidity sensor whether need washing

end
