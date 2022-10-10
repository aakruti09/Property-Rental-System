import sys
import time
import re
from getpass import getpass
from datetime import date
import mysql.connector
from tabulate import tabulate

# def delete_user():
# 	userid = int(input("Please enter the userid to be deleted: "))
# 	mycursor.execute("delete from User where user_id=%s", (userid))
# 	mydb.commit()
# 	if (mycursor.rowcount>0):
# 		print("Successfully deleted the user")
# 	return (['delete_user',1])

def view_property():
	print("===============================")
	print("Please select your preferences to search for rental places in London")
	print("Preferences: Property ID (optional), Min_price, Max_price, Superhost, Duration, Availability, Rating")
	min_price = None
	max_price = None
	superhost = None
	duration = None
	availability = None
	rating = None
	p_id = None
	n = 1
	while(n):
		while(1):
			p_id = input("Property Id (If you want to search for a specific property then enter it's valid property id): ")
			if (re.match("[0-9]+",p_id)):
				mycursor.execute("select listing_id, name, property_type, neighbourhood_cleansed, price, has_availability, review_scores_rating from Property inner join Address using(zipcode) inner join Property_Review_Statistics using(listing_id) where listing_id=%s",(p_id,))
				if (mycursor.rowcount==0):
					print("Error: No property found with property id=",p_id)
					continue
				else:
					result = mycursor.fetchall()
					break
			elif (re.match("",p_id)):
				p_id = None
				break
			else:
				print("Error: Invalid Input. Only numerical values greater than 0 or empty input is allowed")
				continue

		notok = 1
		while(notok):
			if (p_id!=None):
				break
			min_price = input("\nMinimum price (Enter a minimum price per night in US dollars): ")
			try:
				min_price = float(min_price)
				notok = 0
			except ValueError:
				print("Error: Invalid input. Enter only integer or float values")
				continue
		notok = 1
		while(notok):
			if (p_id!=None):
				break
			max_price = input("Maximum price (Enter a maximum price per night in US dollars): ")
			try:
				max_price = float(max_price)
				notok = 0
			except ValueError:
				print("Error: Invalid input. Enter only integer or float values")
				continue
		notok = 1
		while(notok):
			if (p_id!=None):
				break
			superhost = input("Superhost (Enter 1 if you want properties hosted by superhost else 0):  ")
			try:
				superhost = int(superhost)
				if (not(superhost==1 or superhost==0)):
					print("Error: Invalid input. Enter either 1 or 0")
					continue
				else:
					notok = 0
			except ValueError:
				print("Error: Invalid input. Enter either 1 or 0")
				continue
		notok = 1
		while(notok):
			if (p_id!=None):
				break
			duration = input("Duration (Enter number of days you intend to stay):  ")
			try:
				duration = int(duration)
				notok = 0
			except ValueError:
				print("Error: Invalid input. Enter only integer values")
				continue
		notok = 1
		while(notok):
			if (p_id!=None):
				break
			availability = input("Availability (Enter 1 if the properties should be available else 0):  ")
			try:
				availability = int(availability)
				if (not(availability==1 or availability==0)):
					print("Error: Invalid input. Enter either 1 or 0")
					continue
				else:
					notok = 0
			except ValueError:
				print("Error: Invalid input. Enter either 1 or 0")
		while(1):
			if (p_id!=None):
				break
			rating = input("Rating (Enter a minimum rating value out of 100): ")
			if (re.match("^[1]?[0-9]?[0-9]$",rating)):
				break
			else:
				print("Error: Invalid Input. Rating value should be a number from 1 to 100")
				continue
		if (p_id==None):
			mycursor.execute("select listing_id, name, property_type, neighbourhood_cleansed, price, has_availability, review_scores_rating from Property inner join Host using(host_id) inner join Address using(zipcode) inner join Property_Review_Statistics using(listing_id) where price<%s and price>%s and has_availability=%s and host_is_superhost=%s and maximum_nights>%s and minimum_nights<%s and review_scores_rating>=%s limit 50", (max_price, min_price, availability, superhost, duration, duration, int(rating)))
			if (mycursor.rowcount==0):
				print("\nSorry!! No property available as per your preferences")
				while(1):
					option = input("Enter * to select new preferences OR ^ to return to your dashboard: ")
					if (re.match("[*]",option)):
						break
					elif (re.match("[^]",option)):
						return(['view_property', -1])
					else:
						print("Error: Invalid Input. Only * OR ^ is allowed.")
						continue
				if (option=='*'):
					continue
			elif (mycursor.rowcount>0):
				result = mycursor.fetchall()
		# else:
		# 	result = mycursor.fetchall()
		browsing = 1
		i = 0
		while(browsing):
			if (p_id==None):
				mycursor.execute("select listing_id, name, property_type, neighbourhood_cleansed, price, has_availability, review_scores_rating from Property inner join Host using(host_id) inner join Address using(zipcode) inner join Property_Review_Statistics using(listing_id) where price<%s and price>%s and has_availability=%s and host_is_superhost=%s and maximum_nights>%s and minimum_nights<%s and review_scores_rating>=%s limit 50", (max_price, min_price, availability, superhost, duration, duration, int(rating)))
				result = mycursor.fetchall()
			else:
				mycursor.execute("select listing_id, name, property_type, neighbourhood_cleansed, price, has_availability, review_scores_rating from Property inner join Address using(zipcode) inner join Property_Review_Statistics using(listing_id) where listing_id=%s",(p_id,))
				result = mycursor.fetchall()
			print("\nSelect an option from below list of actions")
			print("*: To select new preferences")
			print("^: To go back to your dashboard")
			print("<Property ID>: To select a property enter its corresponding Property ID")
			print("<: To go to previews page")
			print(">: To go to next page\n")
			print("--------------------------------------------------------------------------------------------------")
			print(tabulate(result[i:i+10][:], headers=["Property ID","Name","Property type","Area","Price/night(USD)","Availability","Rating"]))
			# print("Sr No.    | Name    | Property type    | Area    | Price (per night in USD)    | Availability   | Rating  ")
			# for r in result[i:i+10]:
			# 	print(i,' |',r[1],' |',r[2],' |',r[3],' |',r[4],' |',r[5],' |',r[6])
			# 	i = i + 1
			# i = i-10
			print("<Previous Page\t\t\t\t\t\t\t\t\t\tNext Page>")
			print("--------------------------------------------------------------------------------------------------\n")
			option = None
			check = 0
			notok = 1
			while(notok):
				choice = input("Option: ")
				try:
					choice = int(choice)
					for e in result:
						if choice==e[0]:
							notok = 0
							option = choice
							property_id = e[0]
							property_name = e[1]
							price = e[4]
							check=1
					if check==1:
						break
					elif check==0:
						print("Error: Invalid Input. Property Id entered didn't match in the database")
						continue
				except ValueError:
					if (choice not in ['*','^','<','>']):
						print("Error: Invalid input/option. Please enter either a Sr No(i.e. integer) or any of these symbols (*,^,<,>)")
						continue
					else:
						if (choice=='<') and (i<=0):
							print("Cannot go to previous page. This is the first page.")
							continue
						elif (choice=='>') and (i+10>=len(result)):
							print("Cannot go to the Next page. This is the last page.")
							continue
						notok = 0
						option = choice

			if (option=='<'):
				i = i-10
				continue
			elif (option=='>'):
				i = i+10
				continue
			elif (option=='*'):
				break
			elif (option=='^'):
				return (['view_property',-1])
			elif (check==1):
				# property_id = result[option][0]
				# price = result[option][4]
				# accommodates = result[option][6]
				# guests included = result[option][7]
				# extra_people_price = result[option][8]
				print("\nProperty selected is: ",property_name)
				# print("Property id: ", result[option][0])
				mycursor.execute("select user_name, date_of_review, comments from Review inner join Booking using(booking_id) inner join User on(Booking.guest_id=User.user_id) where listing_id=%s order by date_of_review desc limit 10",(property_id,))
				review_result = mycursor.fetchall()

				mycursor.execute("select number_of_reviews, review_scores_rating, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value from Property_Review_Statistics where listing_id=%s",(property_id,))
				rating_result = mycursor.fetchall()

				mycursor.execute("select listing_id, name, property_type, room_type, description, neighbourhood_cleansed, zipcode, neighborhood_overview, transit,  accommodates, guests_included, amenities, bathrooms, bedrooms, beds, bed_type, access, house_rules, notes, minimum_nights, maximum_nights, price, security_deposit, cleaning_fee, extra_people, has_availability, cancellation_policy, required_guest_phone_verification, user_name, host_since, host_location, host_about, host_response_time, host_is_superhost, host_listings_count, host_identity_verified from Property inner join Property_Big_Values using(listing_id) inner join Address using(zipcode) inner join Host using(host_id) inner join User on (host_id = user_id) where listing_id=%s",(property_id,))
				sub_result = mycursor.fetchall()
				accommodates = sub_result[0][9]
				guest_included = sub_result[0][10]
				extra_people_price = sub_result[0][24]
				print("-------------------------------------------------------")
				print("\nName: ",sub_result[0][1])
				print("\nProperty Type: ",sub_result[0][2])
				print("\nRoom Type: ",sub_result[0][3])
				if (sub_result[0][4]==''):
					print("\nDescription: NA")
				else:
					print("\nDescription: ",sub_result[0][4])
				if (sub_result[0][5]==''):
					print("\nArea: NA")
				else:
					print("\nArea: ",sub_result[0][5])
				if (sub_result[0][6]==''):
					print("\nZipcode: NA")
				else:
					print("\nZipcode: ",sub_result[0][6])
				if (sub_result[0][7]==''):
					print("\nNeighbourhood Overivew: NA")
				else:
					print("\nNeighbourhood Overivew: ",sub_result[0][7])
				if (sub_result[0][8]==''):
					print("\nTransit: NA")
				else:
					print("\nTransit: ",sub_result[0][8])
				if (sub_result[0][9]==''):
					print("\nAccommodates: NA")
				else:
					print("\nAccommodates: ",sub_result[0][9],"people")	
				if (sub_result[0][10]==''):
					print("\nGuests included: NA")
				else:
					print("\nGuestes included: ",sub_result[0][10],"guests are allowed other than the number of people accommodated")
				if (sub_result[0][11]==''):
					print("\nAmenities: NA")
				else:
					print("\nAmenities: ",sub_result[0][11])
				if (sub_result[0][12]==''):
					print("\nBathrooms: NA")
				else:
					print("\nBathrooms: ",sub_result[0][12])
				if (sub_result[0][13]==''):
					print("\nBedrooms: NA")
				else:
					print("\nBedrooms: ",sub_result[0][13])
				if (sub_result[0][14]==''):
					print("\nBeds: NA")
				else:
					print("\nBeds: ",sub_result[0][14])
				if (sub_result[0][15]==''):
					print("\nBed Type: NA")
				else:
					print("\nBed Type: ",sub_result[0][15])
				if (sub_result[0][16]==''):
					print("\nAccess: NA")
				else:
					print("\nAccess: ",sub_result[0][16])
				if (sub_result[0][17]==''):
					print("\nHouse Rules: NA")
				else:
					print("\nHouse Rules: ",sub_result[0][17])
				if (sub_result[0][18]==''):
					print("\nNotes: NA")
				else:
					print("\nNotes: ",sub_result[0][18])
				if (sub_result[0][19]==''):
					print("\nMinimum Nights: NA")
				else:
					print("\nMinimum Nights: ",sub_result[0][19])
				if (sub_result[0][20]==''):
					print("\nMaximum Nights: NA")
				else:
					print("\nMaximum Nights: ",sub_result[0][20])
				if (sub_result[0][21]==''):
					print("\nPrice per night: NA")
				else:
					print("\nPrice per night: ",sub_result[0][21],"USD")
				if (sub_result[0][22]==''):
					print("\nSecurity Deposit: NA")
				else:
					print("\nSecurity Deposit: ",sub_result[0][22],"USD")
				if (sub_result[0][23]==''):
					print("\nCleaning Fees: NA")
				else:
					print("\nCleaning Fees: ",sub_result[0][23],"USD")
				if (sub_result[0][24]==''):
					print("\nPrice per night for an extra person: NA")
				else:
					print("\nPrice per night for an extra person: ",sub_result[0][24],"USD")
				if (sub_result[0][25]==''):
					print("\nIs the property available: NA")
				elif (sub_result[0][25]==1):
					print("\nIs the property available: Yes",)
				elif (sub_result[0][25]==0):
					print("\nIs the property available: No",)
				if (sub_result[0][26]==''):
					print("\nCancelation Policy: NA")
				else:
					print("\nCancelation Policy: ",sub_result[0][26])
				has_availability = sub_result[0][25]
				print("\n--------------------")
				print("  Host information")
				print("--------------------")
				if (sub_result[0][28]==''):
					print("\nHost Name: NA")
				else:
					print("\nHost Name: ",sub_result[0][28])
				if (sub_result[0][29]==''):
					print("\nHost Since: NA")
				else:
					print("\nHost Since: ",sub_result[0][29])
				if (sub_result[0][30]==''):
					print("\nHost is from: NA")
				else:
					print("\nHost is from: ",sub_result[0][30])
				if (sub_result[0][31]==''):
					print("\nAbout Host: NA")
				else:
					print("\nAbout Host: ",sub_result[0][31])
				if (sub_result[0][32]==''):
					print("\nHost response time: NA")
				else:
					print("\nHost response time: ",sub_result[0][32])
				if (sub_result[0][33]==''):
					print("\nIs Host a superhost: NA")
				elif (sub_result[0][33]==1):
					print("\nIs Host a superhost: Yes")
				elif (sub_result[0][33]==0):
					print("\nIs Host a superhost: No")
				if (sub_result[0][34]==''):
					print("\nNumber of times host posted a property: NA")
				else:
					print("\nNumber of times host posted a property: ",sub_result[0][34])
				if (sub_result[0][35]==''):
					print("\nIs Host's identity verified: NA")
				elif (sub_result[0][35]==1):
					print("\nIs Host's identity verified: Yes")
				elif (sub_result[0][35]==0):
					print("\nIs Host's identity verified: No")

				print("\n------------------------------------------")
				print("  Property Ratings based on different parameters")
				print("------------------------------------------")
				if (len(rating_result)==0):
					print("No rating data available for this property\n")
				else:
					print(tabulate(rating_result, headers=["# of People Rated","Overall Rating(out of 100)", "Cleanliness", "Checkin","Communication","Location","Value for Money"]))
					print("\n")

				print("\n------------------------------------------")
				print("  Latest Reviews by customers")
				print("------------------------------------------")
				if (len(review_result)==0):
					print("No Reviews provided to this property\n")
				else:
					print(tabulate(review_result, headers=["Reviewer Name","Date of review","Comment"], tablefmt="grid"))
				print("\n-------------------------------------------------------")
				option = None
				print("\n0: To go back to list of properties")
				if (user_type!=2):
					print("1: To book the selected property")
				elif (user_type==2):
					print("-: To delete the selected property from the database")
				while (1):
					option = input("Option: ")
					if (user_type==2 and option=='-'):
						print("Deleting the property")
						mycursor.execute("delete from Property where listing_id=%s",(property_id,))
						mydb.commit()
						print("Successfully deleted the property")
						print("Going back to list of properties...")
						time.sleep(5)
						break
					elif (user_type!=2 and option=='1'):
						if has_availability==0:
							print("Error: You cannot book this property. It is not available.")
							continue
						option = int(option)
						break
					elif (option=='0'):
						option = int(option)
						break
					else:
						print("Error: Invalid Input. Please enter an appropriate input.")
						continue
				if (option==0):
					continue
				elif (option==1):
					booking_date = date.today()
					number_of_people = None
					check_in_date = None
					if (duration==None):
						while(1):
							duration = input("Duration (Enter number of days you intend to stay):  ")
							if (re.match("^[123]?[0-9]?[1-9]$",duration)):
								duration = int(duration)
								break
							else:
								print("Error: Invalid Input. Duration can only have numeric and greater than zero values")
								continue
					notok = 1
					while(notok):
						number_of_people = input("Number of people (Enter the number of people that will stay in the property): ")
						try:
							number_of_people = int(number_of_people)
							if (number_of_people<=0):
								print("Error: Invalid Input. Number of people should be atleast 1")
								continue
							elif (number_of_people>=1):
								notok = 0
						except ValueError:
							print("Error: Invalid Input. Only integer values allowed")
							continue
					notok = 1
					while(notok):
						check_in_date = input("Enter the date you will be checking in (Input format should be YYYY-MM-DD): ")
						if (re.match("[123][0-9]{3}-[01][0-9]-[0123][0-9]",check_in_date)):
							check_in_date = check_in_date.split('-')
							check_in_date = date(int(check_in_date[0]),int(check_in_date[1]),int(check_in_date[2]))
							if (booking_date<=check_in_date):
								notok = 0
							else:
								print("Error: CheckIn date cannot be in past. Please enter a valid check in date")
								continue
						else:
							print("Error: Invalid check_in_date.")
							continue
					mycursor.execute("select weekly_price, monthly_price from Property_OptionalPricing where listing_id=%s",(property_id,))
					if (mycursor.rowcount==0):
						calculated_price = (duration*float(price))
						if (number_of_people>accommodates):
							calculated_price = calculated_price + (number_of_people-accommodates)*float(extra_people_price)*duration
							# print("calculated_price=",calculated_price)
					else:
						temp_result = mycursor.fetchall()
						# print("weekly_price=",temp_result[0][0],"monthly_price=",temp_result[0][1])
						if (temp_result[0][1]!=None and duration>=30):
							monthly_price = float(temp_result[0][1])
							calculated_price = (duration*(monthly_price/30))
							if (number_of_people>accommodates):
								calculated_price = calculated_price + (number_of_people-accommodates)*float(extra_people_price)*duration
						elif (temp_result[0][0]!=None and duration>=7):
							weekly_price = float(temp_result[0][0])
							calculated_price = (duration*(weekly_price/7))
							if (number_of_people>accommodates):
								calculated_price = calculated_price + (number_of_people-accommodates)*float(extra_people_price)*duration
						else:
							calculated_price = (duration*float(price))
							if (number_of_people>accommodates):
								calculated_price = calculated_price + (number_of_people-accommodates)*float(extra_people_price)*duration


					mycursor.execute("insert into Booking (listing_id, guest_id, booking_date, number_of_people, duration, calculated_price, check_in_date, status) values (%s,%s,%s,%s,%s,%s,%s,'Booked')", (property_id, user_id, booking_date, number_of_people, duration, calculated_price, check_in_date))
					mydb.commit()
					mycursor.execute("update Property set has_availability=0 where listing_id=%s",(property_id,))
					mydb.commit()
					print("\nSuccessfully Booked the property. You can view your bookings in the Booking history section")
					print("\n^: To go back to your dashboard")
					print("0: To go back to the list of properties")
					while(1):
						option = input("Option: ")
						if (option=='^'):
							return (['view_property',-1])
						elif (option=='0'):
							break
						else:
							print("Error: Invalid Input. Only ^ OR 0 are allowed.")
							continue
					# if (duration>=30):
					# 	calculated_price = 
					# mycursor.execute("insert into Booking (listing_id, guest_id, booking_date, )")


def provide_review():
	print("\n--------------------------------------------------")
	print("Below is the list of all bookings for which you can provide a review\n")
	while(1):
		mycursor.execute("select booking_id, listing_id, Property.name, booking_date, duration, check_in_date, check_out_date, status from Booking inner join Property using(listing_id) where guest_id=%s and status='Checked out' and booking_id not in (select booking_id from Review)",(user_id,))
		if (mycursor.rowcount==0):
			print("\nNothinng is there to provide review.")
			print("\n^: To go back to your Dashboard")
			while (1):
				option = input("Option: ")
				if (option=='^'):
					return (['provide_review',-1])
				else:
					print("Error: Invalid Input. Only ^ is allowed.")
					continue
		else:
			result = mycursor.fetchall()
			print(tabulate(result, headers=["Booking Id", "Property ID", "Property Name", "Booking Date", "Duration", "CheckIn date", "CheckOut date", "Status"]))
			print("\nTo provide review for a property. Enter it's Booking ID")
			print("^: To go back to your dashboard")
			print("<booking id>: To provide review")
			option = None
			while(1):
				option = input("Option: ")
				if (re.match("[0-9]+",option)):
					# Check if the entered booking id is a valid booking id
					check = 0
					for e in result:
						if int(option)==e[0]:
							booking_id = e[0]
							property_id = e[1]
							property_name = e[2]
							check = 1
					if check==0:
						print("Error: Invalid booking id. Only enter a booking id that is present in the above list")
						continue
					elif check==1:
						print("Selected property's name is: ",property_name)
						mycursor.execute("select number_of_reviews, review_scores_rating, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value from Property_Review_Statistics where listing_id=%s",(property_id,))
						rating_result = mycursor.fetchall()
						num_rating = int(rating_result[0][0])
						avg_rating = int(rating_result[0][1])
						avg_cleanliness = int(rating_result[0][2])
						avg_checkin = int(rating_result[0][3])
						avg_communication = int(rating_result[0][4])
						avg_location = int(rating_result[0][5])
						avg_value = int(rating_result[0][6])
						
						comment = input("Please provide your review for the selected property within 500 words: ")
						while(1):
							rating = input("Overall Rating (Enter a number between 1 and 100): ")
							if (re.match("^[1]?[0-9]?[0-9]$",rating)):
								rating = int(rating)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 100 are allowed")
								continue
						while(1):
							rating_cleanliness = input("Rating for Cleanliness (Enter a number between 1 and 10): ")
							if (re.match("^[1]?[0-9]$",rating_cleanliness)):
								rating_cleanliness = int(rating_cleanliness)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 10 are allowed")
								continue
						while(1):
							rating_checkin = input("Rate your checkin experience (Enter a number between 1 and 10): ")
							if (re.match("^[1]?[0-9]$",rating_checkin)):
								rating_checkin = int(rating_checkin)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 10 are allowed")
								continue
						while(1):
							rating_communication = input("Rating for Communication (Enter a number between 1 and 10): ")
							if (re.match("^[1]?[0-9]$",rating_communication)):
								rating_communication = int(rating_communication)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 10 are allowed")
								continue
						while(1):
							rating_location = input("Rating for Location (Enter a number between 1 and 10): ")
							if (re.match("^[1]?[0-9]$",rating_location)):
								rating_location = int(rating_location)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 10 are allowed")
								continue
						while(1):
							rating_value = input("Rating for Value for Money (Enter a number between 1 and 10): ")
							if (re.match("^[1]?[0-9]$",rating_value)):
								rating_value = int(rating_value)
								break
							else:
								print("Invalid Input. Only numbers from 1 to 10 are allowed")
								continue
						avg_rating = (num_rating*avg_rating + int(rating))/(num_rating+1)
						avg_cleanliness = (num_rating*avg_cleanliness + rating_cleanliness)/(num_rating+1)
						avg_checkin = (num_rating*avg_checkin + rating_checkin)/(num_rating+1)
						avg_communication = (num_rating*avg_communication + rating_communication)/(num_rating+1)
						avg_location = (num_rating*avg_location + rating_location)/(num_rating+1)
						avg_value = (num_rating*avg_value + rating_value)/(num_rating+1)
						num_rating = num_rating + 1
						mycursor.execute("update Property_Review_Statistics set number_of_reviews=%s, review_scores_rating=%s, review_scores_cleanliness=%s, review_scores_checkin=%s, review_scores_communication=%s, review_scores_location=%s, review_scores_value=%s where listing_id=%s",(num_rating, avg_rating, avg_cleanliness, avg_checkin, avg_communication, avg_location, avg_value, property_id))
						mydb.commit()
						mycursor.execute("insert into Review values (%s,%s,%s)",(booking_id, date.today(), comment))
						mydb.commit()
						print("Successfully recorded your review.")
						time.sleep(5)
						break
				elif (option=='^'):
					return (['provide_review',-1])
				else:
					print("Error: Invalid Input. Only valid booking id OR ^ is allowed.")
					continue



def manage_users():
	print("\n----------------------------------------")
	print("		Manage Users")
	print("\n----------------------------------------")
	while(1):
		username = input("Username (If you want to search by user_name then enter a username else press Enter): ")
		if (username==''):
			mycursor.execute("select user_id, user_name, user_type from User limit 200")
		else:
			mycursor.execute("select user_id, user_name, user_type from User where user_name=%s",(username,))
		result = mycursor.fetchall()
		if (len(result)==0):
			print("No users found in the database")
			print("\n^: To go back to your Dashboard")
			while (1):
				option = input("Option: ")
				if (option=='^'):
					return (['manage_users',-1])
				else:
					print("Error: Invalid Input. Only ^ is allowed.")
					continue
		else:
			i = 0
			new_search = 0
			while(1):
				if (new_search==1):
					break
				print("\nUser Type: 0=Customer 1=Host 2=Admin\n")
				print(tabulate(result[i:i+10][:], headers=["User ID", "User Name", "User Type"]))
				print("<Previous Page\t\t\t\t\t\t\t\t\t\tNext Page>")
				print("\n<: To go to Previous page")
				print(">: To go to Next page")
				print("^: To go to your dashboard")
				print("*: To initiate a new search")
				print("<User Id>: To delete a user")
				option = None
				while(1):
					option = input("Option: ")
					if (option=='<'):
						if (i<=0):
							print("Error: Cannot go to previous page. This is the first page")
							continue
						else:
							if (i-10<0):
								i = 0
								break
							else:
								i = i-10
								break
					elif (option=='>'):
						if (i+10>=len(result)):
							print("Error: Cannot go to next page. This is the last page")
							continue
						else:
							i = i+10
							break
					elif (option=='*'):
						new_search = 1
						break
					elif (option=='^'):
						return(['manage_users',-1])
					elif (re.match("[0-9]+",option)):
						check = 0
						for e in result:
							if int(option)==e[0]:
								user_id = e[0]
								user_name = e[1]
								check = 1
						if check==1:
							mycursor.execute("delete from User where user_id=%s",(user_id,))
							mydb.commit()
							print("\nSuccessfully deleted user with User ID=",user_id,"and Username=",user_name," from database")
							new_search=1
							time.sleep(5)
							break
						else:
							print("Error: User ID provided does not match in the database")
							continue
					else:
						print("Error: Invalid Input. Only <, >, ^,*, OR a valid user id is allowed")
						continue

def index_2d(myList, v):
	for e in myList:
		if v in e:
			return myList.index(e)

def view_all_bookings():
	print("\n----------------------------------------")
	print("List of all bookings\n")
	mycursor.execute("select booking_id, listing_id, user_name, booking_date, number_of_people, duration, calculated_price, check_in_date, check_out_date, status from Booking inner join User on(Booking.guest_id=User.user_id) limit 100")
	result = mycursor.fetchall()
	i = 0
	while(1):
		print(tabulate(result[i:i+10][:], headers=["Booking Id","Property ID", "Guest Name", "Booking Date", "People", "Duration", "Price", "CheckIn date", "CheckOut date", "Status"]))
		print("<Previous Page\t\t\t\t\t\t\t\t\t\tNext Page>")
		print("\n<: To go to Previous page")
		print(">: To go to Next page")
		print("^: To go to your dashboard")
		option = None
		while(1):
			option = input("Option: ")
			if (re.match("[<]",option)):
				if (i<=0):
					print("Error: Cannot go to previous page. This is the first page")
					continue
				else:
					if (i-10<0):
						i = 0
						break
					else:
						i = i-10
						break
			elif (re.match("[>]",option)):
				if (i+10>=len(result)):
					print("Error: Cannot go to next page. This is the last page")
					continue
				else:
					i = i+10
					break
			elif (option=='^'):
				return(['view_all_bookings',-1])
			else:
				print("Error: Invalid Input. Only <, >, and ^ is allowed")
				continue


def travel_hist():
	print("\n---------------------------")
	print("   Booking History")
	print("---------------------------")
	while(1):
	  trav_qry=("SELECT booking_id, listing_id, Property.name,booking_date,number_of_people,duration,calculated_price,"
	    "check_in_date,check_out_date,status from Booking inner join Property using (listing_id)"
	    "where guest_id=%s")
	  try:
	    mycursor.execute(trav_qry,(user_id,))
	  except Exception as e:  print('Error:',e)
	  res_trav = mycursor.fetchall()
	  # print(res_cus)
	  print(tabulate(res_trav, headers=["Booking ID", "Property_id", "Property", "Booking Date", 
	                                   "People", "Duration", "Calculated Price", 
	                                   "Checkin Date", "Checkout Date", "Status"]))

	  print("\n^: To go back to your dashboard")
	  print("<booking id><space>1: To Cancle an active booking")
	  print("<booking id><space>2: To Checkout of an active booking")
	  option = None
	  while(1):
	  	option = input("Option: ")
	  	if (re.match("[0-9]+ [12]",option)):
	  		option = option.split()
	  		booking_id = option[0]
	  		mycursor.execute("select booking_id from Booking where booking_id=%s and guest_id=%s",(booking_id,user_id))
	  		if (mycursor.rowcount==0):
	  			pritn("Error: The booking id does not match to any booking id from your booking list. Please enter a valid booking id")
	  			continue
	  		mycursor.execute("select listing_id, check_in_date from Booking where booking_id=%s",(option[0],))
	  		temp_result = mycursor.fetchall()
	  		check_in_date = temp_result[0][1]
	  		property_id = temp_result[0][0]
	  		if (int(option[1])==1):
		  		if (date.today()>check_in_date):
		  			print("Sorry. You cannot cancel this booking. Today's date is greater than or equal to CheckIn date")
		  			continue
		  		else:
		  			mycursor.execute("update Booking set status='Canceled' where booking_id=%s",(option[0],))
		  			mydb.commit()
		  			mycursor.execute("update Property set has_availability=1 where listing_id=%s",(property_id,))
		  			mydb.commit()
		  			print("\nBooking id =",option[0],"is successfully Cancled.")
		  			time.sleep(5)
		  			break
		  	elif (int(option[1])==2):
		  		if (date.today()<=check_in_date):
		  			print("Sorry. You cannot checkout before checking in.")
		  			continue
		  		elif (date.today()>check_in_date):
		  			mycursor.execute("update Booking set status='Checked out', check_out_date=%s where booking_id=%s",(date.today(),option[0]))
		  			mydb.commit()
		  			mycursor.execute("update Property set has_availability=1 where listing_id=%s",(property_id,))
		  			mydb.commit()
		  			print("\nYou have successfully Checked Out for Booking id =",option[0])
		  			time.sleep(5)
		  			break
	  	elif (option=='^'):
	  		return (['travel_hist',-1])
	  	else:
	  		print("Error: Invalid Input. Valid inputs are a valid booking id or this symbol '^'")
	  		continue

def viewRentals():
  host_id = user_id
  print("\n-------------------------")
  print("View all Property Details")
  print("-------------------------\n")
  q1 = ("select listing_id, name, zipcode, property_type, room_type," 
    "guests_included, accommodates, bathrooms, bedrooms, beds, bed_type, minimum_nights," 
    "maximum_nights, experiences_offered, price, cancellation_policy," 
    "security_deposit, cleaning_fee, extra_people, is_location_exact, latitude," 
    "longitude, has_availability, instant_bookable, is_business_travel_ready,"  
    "required_guest_phone_verification from "
    "Property where host_id=%s")
  try:
    mycursor.execute(q1, (host_id,))
  except Exception as e:
    print('Error: ',e)


  # print('Row Count: ',mycursor.rowcount)
  if mycursor.rowcount == 0:
    print("No Properties Yet")
  else:
    result = mycursor.fetchall()
    res=[]
    for a in result:
      b=list(a)
      if (b[19]==1): b[19] = str(b[19]).replace('1','Yes')
      else: b[19] = 'No'
      if (b[22]==1): b[22] = str(b[22]).replace('1','Yes')
      else: b[22] = 'No'
      if (b[23]==1): b[23] = str(b[23]).replace('1','Yes')
      else: b[23] = 'No'
      if (b[24]==1): b[24] = str(b[24]).replace('1','Yes')
      else: b[24] = 'No'
      if (b[25]==1): b[25] = str(b[25]).replace('1','Yes')
      else: b[25] = 'No'
      a = tuple(b)
      # print(a)
      res.append(a)
    # print(res)  
      
    print(tabulate(res, headers=["listing_id", "name", "zipcode", 
      "property_type", "room_type", "guests_included", "accommodates", "bathrooms", "bedrooms", "beds", 
      " bed_type", "minimum_nights", "maximum_nights", "experiences_offered", "price", 
      "cancellation_policy", "security_deposit", "cleaning_fee", "extra_people", 
      "is_location_exact", "latitude", "longitude", "has_availability", "instant_bookable", 
      "is_business_travel_ready", "required_guest_phone_verification"]))
  
  while(1):
    print("\n1. To view more detailed information")
    print("2. To go back\n")
    ch = input("Enter your choice:")
    if ch not in ['1','2']:
      ch = input("Enter valid choice (1 or 2):")
    elif ch == '1':
      lstid = input("Enter listing ID: ")
      #View in detail Optional Pricing Information
      s1 = ("with s1 as (select listing_id from Property where host_id=%s) "
            "select listing_id, weekly_price, monthly_price from s1 "
            "inner join Property_OptionalPricing using (listing_id) where listing_id=%s");
      try:
        mycursor.execute(s1, (host_id,lstid))
        if mycursor.rowcount > 0: 
          print("\n-------------------------------------------") 
          print('Optional Pricing Information about Property')
          print("-------------------------------------------\n")
          s1_res = mycursor.fetchall()
          print(tabulate(s1_res, headers=["Listing ID", "Weekly Price", "Monthly Price"]))
      except Exception as e:
        print('Error:',e)

      print("\n----------------------------------") 
      print('Reviews Statistics about Property')
      print("----------------------------------\n")
      # View Reviews Statistics on Property
      s3 = ("with s1 as (select listing_id from Property where host_id=%s)" 
            "select listing_id, number_of_reviews, number_of_reviews_ltm," 
            "first_review, last_review, review_scores_rating, review_scores_accuracy,"
            "review_scores_cleanliness, review_scores_checkin, review_scores_communication,"
            "review_scores_location, review_scores_value, reviews_per_month from s1 "
            "inner join Property_Review_Statistics using (listing_id) where listing_id=%s;")
      try:
        mycursor.execute(s3, (host_id,lstid))
        s3_res = mycursor.fetchall()
        if mycursor.rowcount > 0:
          print(tabulate(s3_res, headers=["Listing ID", "# Reviews", "# Reviews ltm", "First Review", 
                                          "Last Review", "Rating", "Accuracy", "Cleanliness", 
                                          "CheckIn", "Communication", "Location", "Value", 
                                          "Reviews Per Month"]))
      except Exception as e:
        print('Error:',e)    

      print("\n-----------------------------------") 
      print('Detailed Information about Property')
      print("-----------------------------------\n")
      # View detailed description of Property
      s2 = ("with s1 as (select listing_id from Property where host_id=%s) " 
            "select listing_id, listing_url, space, description, neighborhood_overview," 
            "notes, transit, access, house_rules, picture_url, amenities from s1 "
            "inner join Property_Big_Values using (listing_id) where listing_id=%s")
      try:
        mycursor.execute(s2, (host_id,lstid))
      except Exception as e:
        print('Error:',e)
      
      if mycursor.rowcount > 0: 
          s2_res = mycursor.fetchall()
          print("Listing ID: ",s2_res[0][0])
          print("Listing URL: ",s2_res[0][1])
          print("Space: ",s2_res[0][2])
          print("Description: ",s2_res[0][3])
          print("Neighbourhood Overview: ",s2_res[0][4])
          print("Notes: ",s2_res[0][5])
          print("Transit: ",s2_res[0][6])
          print("Access: ",s2_res[0][7])
          print("House Rules: ",s2_res[0][8])
          print("Picture URL: ",s2_res[0][9])
          ame = s2_res[0][10].strip('{')
          ame = ame.strip('}')
          print("Amenities: ",ame)
        
      #View Reviews
      print("\n---------------------------------") 
      print('Reviews Provided to this Property')
      print("---------------------------------\n")

      s4 = ("with s1 as (select listing_id from Property WHERE host_id=%s), "
            "s2 as (select booking_id from s1 inner join Booking using(listing_id) where listing_id=%s) " 
            "select date_of_review,comments from Review where booking_id in (select booking_id from s2)")

      try:
        mycursor.execute(s4,(host_id,lstid))
        s4_res = mycursor.fetchall()
        if mycursor.rowcount > 0:
          print(tabulate(s4_res, headers=["Date", "Reviews"]))
      except Exception as e:  print('Error:',e)
    elif ch == '2':
      print('Log out')
      break
  # got = host_dashboard(mydb,mycursor,host_id)
  # return got
  return (['viewRentals',-1])

def cust_served():
	host_id = user_id
	cust_qry=("with t1 as (select listing_id from Property where host_id=%s) " 
	"SELECT booking_id, listing_id, user_name, check_out_date, status from "
	"t1 inner join Booking using (listing_id) "
		"inner join User on (Booking.guest_id=User.user_id)")
	try:
		mycursor.execute(cust_qry,(host_id,))
	except Exception as e:  print('Error:',e)
	res_cus = mycursor.fetchall()
	# print(res_cus)
	print(tabulate(res_cus, headers=["Booking ID", "Listing ID", "Guest Name", "Checkout Date", "Status"]))
	# cust_qry=("with t1 as (select listing_id from Property where host_id=%s) " 
	# 	"SELECT booking_id, listing_id, user_name, booking_date, number_of_people, duration,"
	# 	"calculated_price, check_in_date, check_out_date, status from "
	# 	"t1 inner join Booking using (listing_id) "
	# 	"inner join User on (Booking.guest_id=User.user_id)")
	# try:
	# 	mycursor.execute(cust_qry,(host_id,))
	# except Exception as e:  print('Error:',e)
	# res_cus = mycursor.fetchall()
	# # print(res_cus)
	# print(tabulate(res_cus, headers=["Booking ID", "Listing ID", "Guest Name", "Booking Date", 
	#                                "Number of people", "Duration", "Calculated Price", 
	#                                "Checkin Date", "Checkout Date", "Status"]))

	print("\n^: To go back to your Dashboard")
	while (1):
		option = input("Option: ")
		if (option=='^'):
			return (['cust_served',-1])
		else:
			print("Error: Invalid Input. Only ^ is allowed.")
			continue

def insert_new_rental():
  host_id = user_id
  print('Enter New Property Information below as per asked:')
  name = input("Name: ")
  space = input("Space: ")
  description = input("Description: ")
  neighbour = input("Neighbourhood Overview: ")
  neighbour_area = input("Neighbourhood Area Name: ")
  transit = input("Transit Facility: ")
  access = input("What guest can access: ")
  house_rules = input("House Rules: ")
  amenities = input("Amenities enter using ',' such as WiFi, Television: ")
  notes = input("Notes: ")
  street = input('Street: ')
  zipcode = input('Zipcode: ')
  while(1):
    if re.match("^[A-Za-z]{1,2}[0-9]{1,2}( [0-9]{1}[A-Za-z]{2})?$", zipcode):
      break
    else:
      zipcode = input("Enter correct London Zipcode: ")
  market = input('Enter market: ')

  property_type = input("Property Type: ")
  while(1):
    if (len(property_type))>0:
      break
    else:
      property_type = input("Property Type (cannot be null): ")
  room_type = input('Room Type: from these values- Entire home/apt,Private room,Hotel room,Shared room: ')
  while (1):
    if (room_type=="Entire home/apt" or room_type=="Private room" or 
      room_type=="Hotel room" or room_type=="Shared room") :
      break
    else:
      room_type = input('Room Type: from these values- Entire home/apt,Private room,Hotel room,Shared room: ')
  guests = input('Number of Guests included: ')
  while(1):
    if re.match("^\d+$", guests):
      break
    else:
      guests = input('Number of Guests included: ')
  acc = input('Accomodates: ')
  while(1):
    if re.match("^\d+$", acc):
      break
    else:
      acc = input('Accomodates: ')
  bath = input('Number of Bathrooms: ')
  while(1):
    if re.match("^\d+$", bath):
      break
    else:
      bath = input('Number of Bathrooms: ')
  bedrooms = input('Bedrooms: ')
  while(1):
    if re.match("^\d+$", bedrooms):
      break
    else:
      bedrooms = input('Bedrooms: ')
  beds = input('Beds: ')
  bed_type = ""
  while(1):
    if re.match("^\d+$", beds):
      if (int(beds)>1):
        bed_type = input("Enter bed type: ")
      break
    else:
      beds = input('Beds: ')
  min_ni = input('Minimum nights guest can stay: ')
  while(1):
    if re.match("^\d+$", min_ni):
      break
    else:
      min_ni = input('Minimum nights guest can stay: ')
  max_ni = input('Maximum nights guest can stay: ')
  while(1):
    if re.match("^\d+$", max_ni):
      break
    else:
      max_ni = input('Maximum nights guest can stay: ')
  price = input('Price per night: ')
  while(1):
    if re.match("^\d+$", price):
      break
    else:
      price = input('Price per night: ')
  weekly = input('Weekly Price: ')
  while(1):
    if re.match("^\d+$", weekly):
      break
    else:
      weekly = input('Weekly Price: ')
  monthly = input('Monthly Price: ')
  while(1):
    if re.match("^\d+$", monthly):
      break
    else:
      monthly = input('Monthly Price: ')
  security = input('Security Deposit: ')
  while(1):
    if re.match("^\d+$", security):
      break
    else:
      security = input('Security Deposit: ')
  clean = input('Cleaning Fees: ')
  while(1):
    if re.match("^\d+$", clean):
      break
    else:
      clean = input('Cleaning Fees: ')
  extra = input('Extra Person Charge: ')
  while(1):
    if re.match("^\d+$", extra):
      break
    else:
      extra = input('Extra Person Charge: ')
  latitude = input('Latitude: ')
  longitude = input('Longitude: ')
  loc_exact = input('Is Location Exact (Y/N): ')
  while(1):
    if (loc_exact=='Y' or loc_exact=='y'):
      loc_exact=True
      break
    elif (loc_exact=='N' or loc_exact=='n'):
      loc_exact=False
      break
    else:
      loc_exact = input('Is Location Exact (Y/N): ')

  avai = input('Has Availability (Y/N): ')
  while(1):
    if (avai=='Y' or avai=='y'):
      avai=True
      break
    elif (avai=='N' or avai=='n'):
      avai=False
      break
    else:
      avai = input('Has Availability (Y/N): ')

  instant = input('Is Instant Bookable (Y/N): ')
  while(1):
    if (instant=='Y' or instant=='y'):
      instant=True
      break
    elif (instant=='N' or instant=='n'):
      instant=False
      break
    else:
      instant = input('Is Instant Bookable (Y/N): ')

  busi = input('Is Business Travel Ready (Y/N): ')
  while(1):
    if (busi=='Y' or busi=='y'):
      busi=True
      break
    elif (busi=='N' or busi=='n'):
      busi=False
      break
    else:
      busi = input('Is Business Travel Ready (Y/N): ')

  req_ph = input('Required Guest Phone Verification (Y/N): ')
  while(1):
    if (req_ph=='Y' or req_ph=='y'):
      req_ph=True
      break
    elif (req_ph=='N' or req_ph=='n'):
      req_ph=False
      break
    else:
      req_ph = input('Required Guest Phone Verification (Y/N): ')

  cancel = input('Enter cancellation policy (Maximum upto 70 letters): ')
  exper = input('Experiences Offered values from- (family, business, romantic, social, none): ')
  while(1):
    if(exper == "family" or exper == "business" or exper == "romantic" or exper == "social" or exper == "none"):
      break
    else:
      exper = input('Experiences Offered values from- (family, business, romantic, social, none)')

  ins_addr = ("insert into Address "
	"(zipcode, street, city, neighbourhood_cleansed, market, country_code, country) "
	"values (%s, %s, %s, %s, %s, %s, %s)")
  addr_data = (zipcode, street, "London", neighbour_area, market, "GB", "United Kingdom")
  
  try:
      mycursor.execute(ins_addr, addr_data)
      mydb.commit()
  except Exception as e:
      print('Error:',e)
  
  zip_ins = mycursor.lastrowid
  print('Zip code inserted')


  ins_prop = ("insert into Property "
	"(host_id, name, zipcode, property_type, room_type, guests_included,"
	"accommodates, bathrooms, bedrooms, beds, bed_type, minimum_nights,"
	"maximum_nights, price, security_deposit, cleaning_fee, extra_people,is_location_exact,"
  "latitude, longitude, has_availability, instant_bookable,is_business_travel_ready, cancellation_policy,"
	"required_guest_phone_verification, experiences_offered) "
	"values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
  prop_data = (host_id, name, zipcode, property_type, room_type, guests, 
               acc, bath, bedrooms, beds, bed_type, min_ni, max_ni, price, 
               security, clean, extra, loc_exact, latitude, longitude, avai, 
               instant, busi, cancel, req_ph, exper)

  try:
      mycursor.execute(ins_prop, prop_data)
      mydb.commit()
  except Exception as e:
      print('Error:',e)
  
  list_id = mycursor.lastrowid
  print('Property inserted')

  ins_big = ("insert into Property_Big_Values "
	"(listing_id, space, description, neighborhood_overview, notes, transit,"
	"access, house_rules, amenities) "
	"values(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
  
  prop_big_data = (list_id, space, description, neighbour, notes, transit, access, 
	house_rules, amenities)
  try:
      mycursor.execute(ins_big, prop_big_data)
      mydb.commit()
  except Exception as e:
      print('Error:',e)
  print('Big values of Property inserted')


  ins_op_pricing = ("insert into Property_OptionalPricing "
	                  "(listing_id, weekly_price, monthly_price) "
	                  "values (%s, %s, %s)")
  optional_data = (list_id, weekly, monthly)
  try:
    mycursor.execute(ins_op_pricing, optional_data)
    mydb.commit()
  except Exception as e:  print('Error:',e)
  print('Optional pricing of property inserted')

  if mycursor.rowcount==1:
    sel = ("SELECT host_listings_count FROM Host WHERE host_id=%s")
    mycursor.execute(sel, (host_id,))
    
    if (mycursor.rowcount==0):
      print("No rows")
    else:
      result = mycursor.fetchall()
      lst_cnt = result[0][0];
      # print('Fetched Listing Count : ',lst_cnt)
      upd = ("UPDATE Host SET host_listings_count=%s WHERE host_id=%s")
      if (lst_cnt is None): 
        upd_data = (1, host_id)
      else:
        upd_data = (int(lst_cnt)+1, host_id)
      try:
        mycursor.execute(upd,upd_data)
        mydb.commit()
      except Exception as e : print('Error:',e)
      if (mycursor.rowcount==1):
        print("Host Listing Count Data Updated")
      else:
        print("Host Listing Count Not Updated")

  # got = host_dashboard(mydb,mycursor,host_id)
  # return got

  print("\n^: To go back to your Dashboard")
  while (1):
    option = input("Option: ")
    if (option=='^'):
      return (['insert_new_rental',-1])
    else:
      print("Error: Invalid Input. Only ^ is allowed.")
      continue

def del_prop():
  host_id = user_id
  print("\n-------------------------")
  print("View all Properties you own")
  print("-------------------------\n")
  l1 = ("select listing_id, name from Property where host_id=%s")
  try:
    mycursor.execute(l1, (host_id,))
  except Exception as e:
    print('Error: ',e)

  if mycursor.rowcount == 0:
    print("No Properties Yet")
  else:
    l1_res = mycursor.fetchall()
    print(tabulate(l1_res, headers=["Listing_id", "Name"]))
    
    lstiddel=input('Enter Listing ID to delete it:')

    d1 = ("DELETE FROM Property WHERE host_id=%s and listing_id=%s")
    try:
      mycursor.execute(d1,(host_id,lstiddel))
      print('Rows affected:',mycursor.rowcount)
      if (mycursor.rowcount == 1):
        d2 = ("UPDATE Host SET host_listings_count=host_listings_count-1 where host_id=%s")
        try:
          rows2 = mycursor.execute(d2,(host_id,))
          print('Data Updated')
          mydb.commit()
        except Exception as e:  print('Error:',e)
    except Exception as e: print('Error:',e)
  # got = host_dashboard(mydb,mycursor,host_id)
  # return got
  print("\n^: To go back to your Dashboard")
  while (1):
    option = input("Option: ")
    if (option=='^'):
      return (['del_prop',-1])
    else:
      print("Error: Invalid Input. Only ^ is allowed.")
      continue

def edit_profile():
  host_id = user_id
  #View Profile
  print("=================================")
  print("           View Profile          ")
  print("=================================")
  print("Host ID:",host_id)
  view1 = ("SELECT user_name FROM User WHERE user_id=%s")
  try:
    mycursor.execute(view1, (host_id,))
  except Exception as e:
    print('Error:',e)
  view1_res=mycursor.fetchall()
  print("Name:",view1_res[0][0])

  view2 = ("SELECT host_since,host_location,host_about,host_response_time,"
    "host_response_rate,host_is_superhost,host_neighbourhood,host_listings_count,"
    "host_identity_verified FROM Host WHERE host_id=%s")
  try:
    mycursor.execute(view2, (host_id,))
  except Exception as e:
    print('Error:',e)
  view2_res=mycursor.fetchall()
  print("Since:",view2_res[0][0])
  print("Location:",view2_res[0][1])
  print("About:",view2_res[0][2])
  print("Response Time:",view2_res[0][3])
  print("Response Rate:",view2_res[0][4])
  if(view2_res[0][5]==1):   print("Is Superhost: Yes")
  else:    print("Is Superhost: No")
  print("Neighbourhood:",view2_res[0][6])
  print("Number of Properties:",view2_res[0][7])
  if(view2_res[0][8]==1):   print("Identity Verified: Yes")
  else:    print("Identity Verified: No")


  #Edit Profile
  print("=================================")
  print("           Edit Profile          ")
  print("=================================")
  print("Enter number for value you want to edit")
  print("1. Name\n2. Location\n3. About\n4. Response Time\n5. Neighbourhood details\n6. Nothing Else")
  s1=""; s2=""; s3=""; s4=""; s5=""
  while(1):
    choice = int(input("Option: "))
    if isinstance(choice, int)==False:
      print("Error: Invalid choice. Please insert a valid choice(only numbers are valid)")
    elif (choice not in [1,2,3,4,5,6]):
      print("Error: Invalid choice. Please insert a valid choice(only numbers from 1 to 6 are valid)")
    elif (choice == 1):
      name = input('Name: ')
      if (len(name)>0):
        s1 = ("UPDATE User SET user_name = %s WHERE user_id = %s")
        s1_val = (name, host_id)        
        try:
            mycursor.execute(s1, s1_val)
            mydb.commit()
            if(mycursor.rowcount == 1):
              print('Name Data Updated')
            else:
              print('Name Data not Updated')
        except Exception as e:
            print('Error:',e)
               
    elif (choice == 2):
      location = input("Location (Maximum limit- 80 characters): ")
      if (len(location)>0):
        s2 = ("UPDATE Host SET host_location = %s WHERE host_id = %s")
        s2_val = (location, host_id)        
        try:
            mycursor.execute(s2, s2_val)
            mydb.commit()
            if(mycursor.rowcount == 1):
              print('Location Data Updated')
            else:
              print('Location Data not Updated')
        except Exception as e:
            print('Error:',e)

    elif (choice == 3):
      about = input("About: ")
      if (len(about)>0):
        s3 = ("UPDATE Host SET host_about = %s WHERE host_id = %s")
        s3_val = (about, host_id)        
        try:
            mycursor.execute(s3, s3_val)
            mydb.commit()
            if(mycursor.rowcount == 1):
              print('About Data Updated')
            else:
              print('About Data not Updated')
        except Exception as e:
            print('Error:',e)

    elif (choice == 4):
      responseTime = input(("Response Time should be from this values :"
      " (within an hour,within a few hours,within a day,a few days or more): "))      
      while (1):
        if (responseTime=="within an hour" or responseTime=="with a few hours" or 
          responseTime=="within a day" or responseTime=="a few days or more") :
          break
        else:
          responseTime = input(("Response Time should be from this values :"
        " (within an hour,within a few hours,within a day,a few days or more): "))
      
      if (len(responseTime)>0):
        s4 = ("UPDATE Host SET host_response_time = %s WHERE host_id = %s")
        s4_val = (responseTime, host_id)        
        try:
            mycursor.execute(s4, s4_val)
            mydb.commit()
            if(mycursor.rowcount == 1):
              print('Response Time Data Updated')
            else:
              print('Response Time Data not Updated')
        except Exception as e:
            print('Error:',e)

    elif (choice == 5):
      neighbourhood = input("Neighbourhood (Maximum limit- 40 characters): ")
      if (len(neighbourhood)>0):
        s5 = ("UPDATE Host SET host_neighbourhood = %s WHERE host_id = %s")
        s5_val = (neighbourhood, host_id)        
        try:
            mycursor.execute(s5, s5_val)
            mydb.commit()
            if(mycursor.rowcount == 1):
              print('Neighbourhood Data Updated')
            else:
              print('Neighbourhood Data not Updated')
        except Exception as e:
            print('Error:',e)
    
    elif (choice == 6):
      break 

  # got = host_dashboard(mydb,mycursor,host_id)
  # return got
  print("\n^: To go back to your Dashboard")
  while (1):
    option = input("Option: ")
    if (option=='^'):
      return (['edit_profile',-1])
    else:
      print("Error: Invalid Input. Only ^ is allowed.")
      continue


def register_host():
	while(1):
		print('Enter Host Information below as per asked below')
		location = input("Location (Maximum limit- 80 characters): ")
		about = input("About: ")
		responseTime = input(("Response Time should be from this values :"
		  " (within an hour,within a few hours,within a day,a few days or more): "))      
		while (1):
			if (responseTime=="within an hour" or responseTime=="with a few hours" or responseTime=="within a day" or responseTime=="a few days or more"):
				break
			else:
				responseTime = input(("Response Time should be from this values :"
				" (within an hour,within a few hours,within a day,a few days or more): "))

		responseRate = input("Response Rate (format:100.00): ")
		while(1):
			if re.match("^[0-9]{1,3}(.[0-9]{1,2})?$", responseRate):
				break
			else:
				responseRate = input("Response Rate (format:100.00): ")

		neighbourhood = input("Neighbourhood (Maximum limit- 40 characters): ")
		# listingcnt = input("Number of properties: ")
		# while(1):
		# 	if re.match("^\d+$", listingcnt):
		#     	break
		#   	else:
		#     	listingcnt = input("Number of properties: ")
		listingcnt = 0
		insert_host_data = ("INSERT INTO Host" 
		  "(host_id, host_since, host_location, host_about, host_response_time, host_response_rate,"
		  "host_is_superhost, host_neighbourhood, host_listings_count, host_identity_verified,"
		  "host_has_profile_pic) " 
		  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
		  
		# today = datetime.now().date()
		today = date.today()
		data = (user_id, today, location, about, responseTime, responseRate, False, neighbourhood, listingcnt, False, False)
		user_type = 1
		try:
		 	mycursor.execute(insert_host_data, data)
		 	mydb.commit()
		 	mycursor.execute("update User set user_type=1 where user_id=%s",(user_id,))
		 	mydb.commit()
		 	user_type = 1
		 	print("\nCongratulations. You are now a Host. You can now start posting your properties selecting 'Post a New Rental Property' option from your dashboard")
		 	user_type = 1
		 	print("\n^: To go back to your Dashboard")
		 	while(1):
		 		option = input("Option: ")
		 		if (option=='^'):
		 			return (['register_host',-1])
		 		else:
		 			print("Error: Invalid Input. Only ^ is allowed.")
		 			continue
		except Exception as e:
			print('Error:',e)
		break

	# host_id = mycursor.lastrowid
	# if host_id>0:
	# 	print('Your Host ID is:',host_id)
	# return (["Register Host",1,host_id])


def customer_dashboard():
	print("\n\t===============================")
	print("\t     ",user_name+"'s Dashboard")
	print("\t===============================")
	print("Please select the option number from the below listed options of action")
	print("1. Browse and Book rental properties")		#Properties search by rating,property_id,etc
	print("2. Booking history")
	print("3. Provide review for previous bookings")
	print("4. Become a host")
	print("5. Logout\n")
	option = None
	while(1):
		option = input("Option: ")
		if (re.match("[12345]{1}",option)):
			break
		else:
			print("Error: Invalid choice. Please insert a valid choice(only numbers from 1 to 5 are valid)")
			continue
	return (['customer_dashboard',int(option)])

def host_dashboard():
	print("\n\t===============================")
	print("\t     ",user_name+"'s (Host) Dashboard")
	print("\t===============================")
	print("Please select the option number from the below listed options of action")
	print("1. View Properties Details and Reviews")
	print("2. Customers Served History")
	print("3. Browse rental properties and book")   # Booking portion from User
	print("4. Own Travel Rental History (Booking History)")           # Booking History from User
	print("5. Add New Rental Property")
	print("6. Delete Rental Property")
	print("7. View and Edit Profile")
	print("8. Logout\n")
	option = None
	# A brief parser to valid the user input
	while(1):
		option = input("Option: ")
		if (re.match("[12345678]{1}",option)):
			break
		else:
			print("Error: Invalid choice. Please insert a valid choice(only numbers from 1 to 7 are valid)")
			continue
	return (['host_dashboard', int(option)])

def admin_dashboard():
	print("\n\t===============================")
	print("\t     Admin's Dashboard")
	print("\t===============================")
	print("Please select the option number from the below listed options of action")
	print("1. Browse and Manage rental properties")		# View and delete properties
	print("2. View Booking history")
	print("3. Manage Users")
	print("4. Logout\n")
	option = None
	# A brief parser to validate the user input
	while(1):
		option = input("Option: ")
		if (re.match("[1234]{1}",option)):
			break
		else:
			print("Error: Invalid choice. Please insert a valid choice(only numbers from 1 to 4 are valid)")
			continue
	return (['admin_dashboard', int(option)])

def login():
	notok = 1
	try_count = 3
	while(notok and try_count):
		print("-------------------------------")
		print("===============================")
		username = input("Please enter your username: ")
		try:
		    password = getpass()
		    print("===============================")
		    print("-------------------------------")
		except Exception as error:
		    print('ERROR', error)
		try:
			mycursor.execute("select user_name, user_id, user_type from user where user_name=%s AND user_password=%s",(username, password))
	        # NB : you won't get an IntegrityError when reading
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			print(e)
			# return None
		# result = mycursor.execute("select host_name, host_id from Host where host_name='{0}' AND host_id={1}".format(username, password))
		if mycursor.rowcount == 1:
			print("Login Successfull")
			notok = 0
			result = mycursor.fetchall()
			return (['login', result[0][0], result[0][1], result[0][2]])      	#User type: 0 = customer, 1 = host, 2 = admin
		else:
			print("Error: Login Failed. Username or password was incorrect.")
			try_count = try_count - 1
			print(try_count, "tries left")
			if(try_count==0):
				print("All tries exhausted. Closing the Application...")
				time.sleep(3)
				exit()

def register():
	print("Please enter the following information to register")
	print("\n^: Enter ^ to abort registration and go back to home page")
	notok = 1
	username = None
	while(notok):
		username = input("Username: ")
		if (re.match("[_a-zA-Z\s]+",username)):
			mycursor.execute("select user_name from User where user_name=%s",(username,))
			if (mycursor.rowcount>0):
				print("Error: Username", username,"already exists. Please enter another username")
				continue
			else:
				notok = 0
		elif (username=='^'):
			print("Registration aborted. Returning to home page...")
			time.sleep(3)
			return (['register',1])
		else:
			print("Error: Username should only contain alphabets, whitespaces OR _")
			continue

	notok = 1
	password = getpass("Password: ")
	while(notok):
		re_password = getpass("Confirm Password: ")
		if (password!=re_password):
			print("Error: Password does not match with Confirm Password. Please renter Confirm Password")
		elif (password=='^'):
			print("Registration aborted. Returning to home page...")
			time.sleep(5)
			return (['register',1])
		else:
			notok = 0
			mycursor.execute("insert into User (user_name, user_password, user_type) values (%s, %s, 0)", (username, password))
			mydb.commit()
			if (mycursor.rowcount==1):
				print("Successfully registered. Please Login to use the application.")
				# return (['register', 1])
			else:
				print("Error: Database error. Could not insert the data.")
				# return (['register', 0])
	print("\n^: To go back to home page")
	while (1):
		option = input("Option: ")
		if (option=='^'):
			return (['register',1])
		else:
			print("Error: Invalid Input. Only ^ is allowed")
			continue

def home():
	print("\t\t\t======================================")
	print("\t\t\tWelcome to Property Rental Application")
	print("\t\t\t======================================")
	print("\nPlease select one of the below mentioned action")
	print("1. Login")
	print("2. Register")
	print("3. Close the Application\n")

	notok = 1
	option = 0
	while(notok):
		choice = int(input("Option: "))
		if(choice not in [1,2,3]):
			print("Error: Invalid choice. Please provide a valid choice")
			continue
		elif(choice in [1,2,3]):
			notok = 0
			option = choice
	return (['home', option])


if __name__ == "__main__":
	mydb = mysql.connector.connect(
	  host="marmoset03.shoshin.uwaterloo.ca",
	  user="<username>",
	  password="<user_password>",
	  database="db656_aaambasa"
	)
	mycursor = mydb.cursor(buffered=True)
	
	# Router
	user_id = None
	user_type = None
	user_name = None
	return_result = home()
	while(1):
		if (return_result[0]=='home'):
			# print("inside home condition")
			if (return_result[1]==1):
				return_result = login()
				continue
			elif (return_result[1]==2):
				return_result = register()
				continue
			elif (return_result[1]==3):
				exit()
		elif (return_result[0]=='register'):
			# print("inside register condition")
			if ((return_result[1]==1) or (return_result[1]==0)):
				return_result = home()
				continue
		elif (return_result[0]=='login'):
			# print("inside login condition")
			user_id = return_result[2]
			user_type = return_result[3]
			user_name = return_result[1]
			if (return_result[3]==0):					# User type: 0 = customer
				return_result = customer_dashboard()
				continue
			elif (return_result[3]==1):					# User type: 1 = host
				return_result = host_dashboard()
				continue
			elif (return_result[3]==2):
				return_result = admin_dashboard()
				continue
		elif (return_result[0]=='customer_dashboard'):
			# print("inside customer_dashboard condition")
			if (return_result[1]==1):
				return_result = view_property()
				continue
			elif (return_result[1]==2):
				return_result = travel_hist()
				continue
			elif (return_result[1]==3):
				return_result = provide_review()
				continue
			elif (return_result[1]==4):
				return_result = register_host()
				continue
			elif (return_result[1]==5):
				user_id = None
				user_type = None
				user_name = None
				return_result = home()
				continue
		elif (return_result[0]=='host_dashboard'):
			# print("inside host_dashboard condition")
			if (return_result[1]==1):
				return_result = viewRentals()
				continue
			elif (return_result[1]==2):
				return_result = cust_served()
				continue
			elif (return_result[1]==3):
				return_result = view_property()
				continue
			elif (return_result[1]==4):
				return_result = travel_hist()
				continue
			elif (return_result[1]==5):
				return_result = insert_new_rental()
				continue
			elif (return_result[1]==6):
				return_result = del_prop()
				continue
			elif (return_result[1]==7):
				return_result = edit_profile()
				continue
			elif (return_result[1]==8):
				user_id = None
				user_type = None
				user_name = None
				return_result = home()
				continue
		elif (return_result[0]=='admin_dashboard'):
			if (return_result[1]==1):
				return_result = view_property()
				continue
			elif (return_result[1]==2):
				return_result = view_all_bookings()
				continue
			elif (return_result[1]==3):
				return_result = manage_users()
				continue
			elif (return_result[1]==4):
				user_id = None
				user_type = None
				user_name = None
				return_result = home()
				continue
		elif (return_result[0]=='view_property') or (return_result[0]=='travel_hist') or (return_result[0]=='viewRentals') or (return_result[0]=='register_host') or (return_result[0]=='cust_served') or (return_result[0]=='manage_users') or (return_result[0]=='provide_review') or (return_result[0]=='view_all_bookings') or (return_result[0]=='insert_new_rental') or (return_result[0]=='edit_profile') or (return_result[0]=='del_prop'):
			# print("inside view_property condition")
			if (return_result[1]==-1):
				if (user_type==0):
					return_result = customer_dashboard()
					continue
				elif (user_type==1):
					return_result = host_dashboard()
					continue
				elif (user_type==2):
					return_result = admin_dashboard()
					continue