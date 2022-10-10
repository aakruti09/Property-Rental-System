drop table if exists Review;
drop table if exists Booking;
drop table if exists Property_Review_Statistics;
drop table if exists Property_Big_Values;
drop table if exists Property_OptionalPricing;
drop table if exists Property;
drop table if exists Address;
drop table if exists HostVerifications;
drop table if exists Host;
drop table if exists User;

-- /var/lib/mysql-files/Group9/listings.csv

SELECT "CREATE TABLE User" AS " ";
CREATE TABLE User (user_id int PRIMARY KEY AUTO_INCREMENT,
        user_name char(50),
        user_password char(20),
        user_type int
);

load data infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
    into table User
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@id,@listing_url,@scrape_id, @last_scraped,@name,@summary, @space, @description, @experiences_offered, @neighborhood_overview, @notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, @host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, @host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count,  @host_total_listings_count, @host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, @neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude, @is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms,  @beds,@bed_type, @amenities, @square_feet, @price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included,  @extra_people,  @minimum_nights,  @maximum_nights,  @minimum_minimum_nights,  @maximum_minimum_nights,  @minimum_maximum_nights,  @maximum_maximum_nights, @minimum_nights_avg_ntm,  @maximum_nights_avg_ntm,  @calendar_updated, @has_availability, @availability_30,  @availability_60, @vailability_90,  @availability_365,  @calendar_last_scraped, @number_of_reviews,@number_of_reviews_ltm,  @first_review, @last_review, @review_scores_rating,  @review_scores_accuracy,  @review_scores_cleanliness,  @review_scores_checkin,  @eview_scores_communication, @review_scores_location,  @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, @cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, @calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, @reviews_per_month)
        set user_id = @host_id,
            user_name = NULLIF(@host_name,''),
            user_type = 1,
            user_password = @host_id;

load data infile '/var/lib/mysql-files/Group9/reviews.csv' ignore 
    into table User
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@listing_id, @id, @date, @reviewer_id, @reviewer_name, @comments)
        set user_id = @reviewer_id,
            user_name = @reviewer_name,
            user_type = 0,
            user_password = @reviewer_id;

insert into User (user_name, user_password, user_type) values ('admin', 'root@admin', 2);
-- Number of Customers (user_type=0) = 1229153
-- Number of Host (user_type=1) = 53476

SELECT "CREATE TABLE Host" AS " ";
CREATE TABLE Host (
     host_id int PRIMARY KEY,
     host_since date,
     host_location varchar(80),
     host_about text,
     host_response_time ENUM('within an hour', 'within a few hours', 'within a day','a few days or more'),
     host_response_rate decimal(5,2),
     host_is_superhost boolean,
     host_neighbourhood char(40),
     host_listings_count int,
     host_identity_verified boolean,
     host_has_profile_pic boolean,
    email_verified boolean,
    phone_verified boolean,
    google_verified boolean,
    review_verified boolean,
    work_emai_verified boolean,
    facebook_verified boolean,
    identity_manual_verified boolean, 
    jumio_verified boolean,
    govt_id_verified boolean,
    govt_id_offline_verified boolean,
    selfie_verified boolean,
    CHECK (host_response_rate<=100.00),
    foreign key (host_id) references User(user_id) ON UPDATE CASCADE ON DELETE CASCADE);


-- /var/lib/mysql-files/NHL_656/player_info.csv
-- /var/lib/mysql-files/Group9
load data 
     infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
    into table Host 
     fields terminated by ',' 
     enclosed by '"' 
     lines terminated by '\n'
     ignore 1 lines 
     (@id, @listing_url, @scrape_id, @last_scraped, @name, @summary, @space, @description, @experiences_offered, @neighborhood_overview, @notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, @host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, @host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count, @host_total_listings_count, @host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, @neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude, @is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms, @beds, @bed_type, @amenities, @square_feet, @price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included, @extra_people, @minimum_nights, @maximum_nights, @minimum_minimum_nights, @maximum_minimum_nights, @minimum_maximum_nights, @maximum_maximum_nights, @minimum_nights_avg_ntm, @maximum_nights_avg_ntm, @calendar_updated, @has_availability, @availability_30, @availability_60, @availability_90, @availability_365, @calendar_last_scraped, @number_of_reviews, @number_of_reviews_ltm, @first_review, @last_review, @review_scores_rating, @review_scores_accuracy, @review_scores_cleanliness, @review_scores_checkin, @review_scores_communication, @review_scores_location, @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, @cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, @calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, @reviews_per_month) 
     SET 
     host_id = @host_id,
     host_since = NULLIF(@host_since,''), 
     host_location = NULLIF(@host_location,''), 
     host_about = NULLIF(@host_about,''),
     host_response_time = CASE 
          WHEN @host_response_time = '' THEN NULL 
          WHEN @host_response_time = 'N/A' THEN NULL
          ELSE @host_response_time 
     END,
     host_response_rate = CASE 
          WHEN @host_response_rate REGEXP '^[0-9]+%$' THEN REGEXP_SUBSTR(@host_response_rate, '^[0-9]+') 
          ELSE NULL 
     END,
     host_is_superhost = CASE 
          WHEN @host_is_superhost = 't' THEN true 
          WHEN @host_is_superhost = 'f' THEN false 
          ELSE NULL
     END,
     host_neighbourhood = NULLIF(@host_neighbourhood,''), 
     host_listings_count = @host_listings_count, 
     host_identity_verified = CASE 
          WHEN @host_identity_verified = 't' THEN true 
          WHEN @host_identity_verified = 'f' THEN false 
          ELSE NULL 
     END,
     host_has_profile_pic = CASE 
          WHEN @host_has_profile_pic = 't' THEN true 
          WHEN @host_has_profile_pic = 'f' THEN false 
          ELSE NULL 
     END,
    email_verified = CASE WHEN @host_verifications like '%email%' THEN TRUE ELSE FALSE END, 
    phone_verified = CASE WHEN @host_verifications like '%phone%' THEN TRUE ELSE FALSE END,
    google_verified = CASE WHEN @host_verifications like '%google%' THEN TRUE ELSE FALSE END,
    review_verified = CASE WHEN @host_verifications like '%reviews%' THEN TRUE ELSE FALSE END,
    work_emai_verified = CASE WHEN @host_verifications like '%work_email%' THEN TRUE ELSE FALSE END,
    facebook_verified = CASE WHEN @host_verifications like '%facebook%' THEN TRUE ELSE FALSE END,
    identity_manual_verified = CASE WHEN @host_verifications like '%identity_manual%' THEN TRUE ELSE FALSE END,
    jumio_verified = CASE WHEN @host_verifications like '%jumio%' THEN TRUE ELSE FALSE END,
    govt_id_verified = CASE WHEN @host_verifications like '%government_id%' THEN TRUE ELSE FALSE END,
    govt_id_offline_verified = CASE WHEN @host_verifications like '%offline_government_id%' THEN TRUE ELSE FALSE END,
    selfie_verified = CASE WHEN @host_verifications like '%selfie%' THEN TRUE ELSE FALSE END;



select 'Create table Address' as ' ';
create table Address (
    zipcode char(10),
    street varchar(80),
    city char(40),
    neighbourhood_cleansed char(25),
    market char(30), 
    country_code char(8),
    country char(15),
    UNIQUE KEY (zipcode));


load data 
    infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
    into table Address 
    fields terminated by ',' 
    enclosed by '"' 
    lines terminated by '\n'
    ignore 1 lines 
    (@id, @listing_url, @scrape_id, @last_scraped, @name, @summary, @space, @description, @experiences_offered, @neighborhood_overview, @notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, @host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, @host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count, @host_total_listings_count, @host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, @neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude, @is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms, @beds, @bed_type, @amenities, @square_feet, @price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included, @extra_people, @minimum_nights, @maximum_nights, @minimum_minimum_nights, @maximum_minimum_nights, @minimum_maximum_nights, @maximum_maximum_nights, @minimum_nights_avg_ntm, @maximum_nights_avg_ntm, @calendar_updated, @has_availability, @availability_30, @availability_60, @availability_90, @availability_365, @calendar_last_scraped, @number_of_reviews, @number_of_reviews_ltm, @first_review, @last_review, @review_scores_rating, @review_scores_accuracy, @review_scores_cleanliness, @review_scores_checkin, @review_scores_communication, @review_scores_location, @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, @cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, @calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, @reviews_per_month) 
    SET     
    zipcode = CASE 
        WHEN @zipcode regexp '^[A-Za-z]{1,2}[0-9]{1,2} ([0-9]{1}[A-Za-z]{2})?$' THEN @zipcode 
        ELSE NULL
    END,
    street = CASE
        WHEN trim(@street regexp '^[A-Za-z0-9 -,.]+$') THEN 
        nullif(trim(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            regexp_replace(
                                replace(
                                    replace(
                                        regexp_replace(
                                            regexp_replace(
                                                replace(
                                                    replace(@street,'United Kingdom','')
                                                ,'Greater London','')
                                            ,'london','')
                                        ,'England','')
                                    ,',','')
                                ,'.','')
                            ,'gb','')
                        ,'uk','')
                    ,'londra','') 
                ,'londres','')
            ,'city','')
        ),'')
        WHEN @street regexp '[A-Za-z]+[0-9]+' THEN trim(regexp_replace(@street,'[A-Z]{5,10}$',''))
        ELSE NULL
    END,
    city = CASE
        WHEN (lower(@street) LIKE '%great%') THEN 'Greater London'   
        else 'London'
    END,
    neighbourhood_cleansed = @neighbourhood_cleansed,
    market = NULLIF(@market,''),
    country_code = @country_code,  
    country = @country;
update Address set street=NULL where regexp_substr(street,'^[A-Za-z0-9 -,.*]{1,3}$') is not null;


SELECT "CREATE TABLE Property" AS " ";
CREATE TABLE Property (listing_id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(255), 
    host_id int,
    zipcode char(10),
    property_type char(25) NOT NULL,
    room_type enum('Entire home/apt','Private room','Hotel room','Shared room'),
    guests_included int,
    accommodates int NOT NULL,
    bathrooms int,
    bedrooms int,
    beds int,
    bed_type char(15),
    minimum_nights int NOT NULL,
    maximum_nights int NOT NULL,
    price decimal(7,2) NOT NULL,
    security_deposit decimal(7,2),
    cleaning_fee decimal(6,2),
    extra_people decimal(6,2) NOT NULL,
    is_location_exact boolean,
    latitude decimal(12,7),
    longitude decimal(12,7),
    has_availability boolean,   
    instant_bookable boolean,
    is_business_travel_ready boolean,
    cancellation_policy char(70),
    required_guest_phone_verification boolean,
    experiences_offered char(10), 
    FOREIGN KEY (host_id) REFERENCES Host(host_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (zipcode) REFERENCES Address(zipcode) ON UPDATE CASCADE ON DELETE RESTRICT);


load data 
    infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
    into table Property 
    fields terminated by ',' 
    enclosed by '"' 
    lines terminated by '\n'
    ignore 1 lines 
    (@id, @listing_url, @scrape_id, @last_scraped, @name, @summary, @space, @description, @experiences_offered, @neighborhood_overview, @notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, @host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, @host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count, @host_total_listings_count, @host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, @neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude, @is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms, @beds, @bed_type, @amenities, @square_feet, @price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included, @extra_people, @minimum_nights, @maximum_nights, @minimum_minimum_nights, @maximum_minimum_nights, @minimum_maximum_nights, @maximum_maximum_nights, @minimum_nights_avg_ntm, @maximum_nights_avg_ntm, @calendar_updated, @has_availability, @availability_30, @availability_60, @availability_90, @availability_365, @calendar_last_scraped, @number_of_reviews, @number_of_reviews_ltm, @first_review, @last_review, @review_scores_rating, @review_scores_accuracy, @review_scores_cleanliness, @review_scores_checkin, @review_scores_communication, @review_scores_location, @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, @cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, @calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, @reviews_per_month) 
    SET listing_id = @id, 
    name = @name,
    host_id = @host_id,  
    zipcode = CASE 
        WHEN @street regexp '^[A-Za-z]+[0-9]+' then trim(regexp_replace(@street,'[A-Z]{5,10}$',''))
        WHEN @zipcode regexp '^[A-Za-z]{1,2}[0-9]{1,2} ([0-9]{1}[A-Za-z]{2})?$' THEN @zipcode 
        ELSE NULL
    END,
    property_type = @property_type,
    room_type = @room_type,
    guests_included = @guests_included,
    accommodates = @accommodates,
    bathrooms = if(@bathrooms = '', null, @bathrooms),
    bedrooms = if(@bedrooms = '', null, @bedrooms),
    beds = if(@beds = '', null, @beds),
    bed_type = @bed_type,
    minimum_nights = @minimum_nights,
    maximum_nights = @maximum_nights,
    price = CASE 
        WHEN @price REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@price,'[$,]','') 
        ELSE NULL
        END,
    security_deposit = CASE 
        WHEN @security_deposit REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@security_deposit,'[$,]','') 
        ELSE NULL
        END,
    cleaning_fee = CASE 
        WHEN @cleaning_fee REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@cleaning_fee,'[$,]','') 
        ELSE NULL
        END,
    extra_people = CASE 
        WHEN @extra_people REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@extra_people,'[$,]','')
        ELSE NULL 
        END,
    is_location_exact = CASE 
        WHEN @is_location_exact='t' THEN true 
        WHEN @is_location_exact='f' THEN false
        ELSE NULL
    END,
    latitude = @latitude,
    longitude = @longitude, 
    has_availability = if(@has_availability = 't', TRUE, FALSE),
    instant_bookable = CASE 
        WHEN @instant_bookable='t' THEN true 
        WHEN @instant_bookable='f' THEN false
        ELSE NULL
    END,
    is_business_travel_ready = CASE 
        WHEN @is_business_travel_ready='t' THEN true 
        WHEN @is_business_travel_ready='f' THEN false
        ELSE NULL
    END,
    cancellation_policy = @cancellation_policy,
    required_guest_phone_verification = CASE 
        WHEN @required_guest_phone_verification='t' THEN true 
        WHEN @required_guest_phone_verification='f' THEN false
        ELSE NULL
    END,
    experiences_offered = @experiences_offered;


SELECT "CREATE TABLE Property_OptionalPricing" AS " ";
create table Property_OptionalPricing (listing_id int primary key,
        weekly_price decimal(7,2),
        monthly_price decimal(7,2),
        check((weekly_price IS NOT NULL) OR (monthly_price IS NOT NULL)),
        foreign key (listing_id) references Property(listing_id) ON UPDATE CASCADE ON DELETE CASCADE);

load data infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
     into table Property_OptionalPricing
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@id,@listing_url,@scrape_id, @last_scraped,@name,@summary, @space, @description, @experiences_offered, @neighborhood_overview, 
@notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, 
@host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, 
@host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count,  @host_total_listings_count,  
@host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, 
@neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude,  
@is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms,  @beds,@bed_type, @amenities, @square_feet, 
@price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included,  @extra_people,  @minimum_nights,  
@maximum_nights,  @minimum_minimum_nights,  @maximum_minimum_nights,  @minimum_maximum_nights,  @maximum_maximum_nights, @minimum_nights_avg_ntm,  
@maximum_nights_avg_ntm,  @calendar_updated, @has_availability, @availability_30,  @availability_60, @vailability_90,  
@availability_365,  @calendar_last_scraped, @number_of_reviews,@number_of_reviews_ltm,  @first_review, @last_review, 
@review_scores_rating,  @review_scores_accuracy,  @review_scores_cleanliness,  @review_scores_checkin,  @eview_scores_communication,  
@review_scores_location,  @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, 
@cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, 
@calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, 
@reviews_per_month)
        set listing_id = @id,
            weekly_price = CASE 
                WHEN @weekly_price REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@weekly_price,'[$,]','') 
                ELSE NULL
                END,
            monthly_price = CASE 
                WHEN @monthly_price REGEXP '^[$][0-9]+[,]?[0-9]*[.][0-9]+' THEN REGEXP_REPLACE(@monthly_price,'[$,]','') 
                ELSE NULL
                END;
/*
91.35% data in the property table has weekly_price and monthly_price NULL at the same time
Therefore, we decided to include both the optional pricing attribute in a same table
*/

SELECT "CREATE TABLE Property_Big_Values" AS " ";
create table Property_Big_Values (listing_id int primary key,
    listing_url char(45),
    space varchar(1000),
    description varchar(1000),
    neighborhood_overview varchar(1000),
    notes varchar(1000),
    transit varchar(1000),
    access varchar(1000),
    house_rules varchar(1000),
    picture_url varchar(255),
    amenities varchar(1500),
    foreign key (listing_id) references Property(listing_id) ON UPDATE CASCADE ON DELETE CASCADE);

load data infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
        into table Property_Big_Values
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@id,@listing_url,@scrape_id, @last_scraped,@name,@summary, @space, @description, @experiences_offered, @neighborhood_overview, 
@notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, 
@host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, 
@host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count,  @host_total_listings_count,  
@host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, 
@neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude,  
@is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms,  @beds,@bed_type, @amenities, @square_feet, 
@price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included,  @extra_people,  @minimum_nights,  
@maximum_nights,  @minimum_minimum_nights,  @maximum_minimum_nights,  @minimum_maximum_nights,  @maximum_maximum_nights, @minimum_nights_avg_ntm,  
@maximum_nights_avg_ntm,  @calendar_updated, @has_availability, @availability_30,  @availability_60, @vailability_90,  
@availability_365,  @calendar_last_scraped, @number_of_reviews,@number_of_reviews_ltm,  @first_review, @last_review, 
@review_scores_rating,  @review_scores_accuracy,  @review_scores_cleanliness,  @review_scores_checkin,  @eview_scores_communication,  
@review_scores_location,  @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, 
@cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, 
@calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, 
@reviews_per_month)
        set listing_id = @id,
            listing_url = @listing_url,
            space = @space,
            description = @description,
            neighborhood_overview = @neighborhood_overview,
            notes = @notes,
            transit = @transit,
            access = @access,
            house_rules = @house_rules,
            picture_url = @picture_url,
            amenities = REGEXP_REPLACE(@amenities, '["]','');


SELECT "CREATE TABLE Property_Review_Statistics" AS " ";
create table Property_Review_Statistics (listing_id int primary key,
    number_of_reviews int,
    number_of_reviews_ltm int,
    first_review date,
    last_review date,
    review_scores_rating int,
    review_scores_accuracy int,
    review_scores_cleanliness int,
    review_scores_checkin int,
    review_scores_communication int,
    review_scores_location int,
    review_scores_value int,
    reviews_per_month decimal(5,2),
    foreign key (listing_id) references Property(listing_id) ON UPDATE CASCADE ON DELETE CASCADE);

/* Access to this table is only to Admin, host cannot change review scores which are provided by users, but can only view it. */

load data 
    infile '/var/lib/mysql-files/Group9/listings.csv' ignore 
    into table Property_Review_Statistics 
    fields terminated by ',' 
    enclosed by '"' 
    lines terminated by '\n'
    ignore 1 lines 
    (@id, @listing_url, @scrape_id, @last_scraped, @name, @summary, @space, @description, @experiences_offered, @neighborhood_overview, @notes, @transit, @access, @interaction, @house_rules, @thumbnail_url, @medium_url, @picture_url, @xl_picture_url, @host_id, @host_url, @host_name, @host_since, @host_location, @host_about, @host_response_time, @host_response_rate, @host_acceptance_rate, @host_is_superhost, @host_thumbnail_url, @host_picture_url, @host_neighbourhood, @host_listings_count, @host_total_listings_count, @host_verifications, @host_has_profile_pic, @host_identity_verified, @street, @neighbourhood, @neighbourhood_cleansed, @neighbourhood_group_cleansed, @city, @state, @zipcode, @market, @smart_location, @country_code, @country, @latitude, @longitude, @is_location_exact, @property_type, @room_type, @accommodates, @bathrooms, @bedrooms, @beds, @bed_type, @amenities, @square_feet, @price, @weekly_price, @monthly_price, @security_deposit, @cleaning_fee, @guests_included, @extra_people, @minimum_nights, @maximum_nights, @minimum_minimum_nights, @maximum_minimum_nights, @minimum_maximum_nights, @maximum_maximum_nights, @minimum_nights_avg_ntm, @maximum_nights_avg_ntm, @calendar_updated, @has_availability, @availability_30, @availability_60, @availability_90, @availability_365, @calendar_last_scraped, @number_of_reviews, @number_of_reviews_ltm, @first_review, @last_review, @review_scores_rating, @review_scores_accuracy, @review_scores_cleanliness, @review_scores_checkin, @review_scores_communication, @review_scores_location, @review_scores_value, @requires_license, @license, @jurisdiction_names, @instant_bookable, @is_business_travel_ready, @cancellation_policy, @require_guest_profile_picture, @require_guest_phone_verification, @calculated_host_listings_count, @calculated_host_listings_count_entire_homes, @calculated_host_listings_count_private_rooms, @calculated_host_listings_count_shared_rooms, @reviews_per_month) 
    SET listing_id = @id, 
    number_of_reviews = NULLIF(@number_of_reviews,''),
    number_of_reviews_ltm = NULLIF(@number_of_reviews_ltm,''),
    first_review = NULLIF(@first_review,''),
    last_review = NULLIF(@last_review,''),
    review_scores_rating = NULLIF(@review_scores_rating,''),
    review_scores_accuracy = NULLIF(@review_scores_accuracy,''),
    review_scores_cleanliness = NULLIF(@review_scores_cleanliness,''),
    review_scores_checkin = NULLIF(@review_scores_checkin,''),
    review_scores_communication = NULLIF(@review_scores_communication,''),
    review_scores_location = NULLIF(@review_scores_location,''),
    review_scores_value = NULLIF(@review_scores_value,''),
    reviews_per_month = NULLIF(@reviews_per_month,'');

SELECT "CREATE TABLE Booking" AS " ";
CREATE TABLE Booking (booking_id int PRIMARY KEY AUTO_INCREMENT,
        listing_id int,
        guest_id int,
        booking_date date,
        number_of_people int,
        duration int,
        calculated_price decimal(7,2),
        check_in_date date,
        check_out_date date,
        status enum('Waiting for approval','Booked','Checked out','Canceled'),
        FOREIGN KEY (listing_id) REFERENCES Property(listing_id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (guest_id) REFERENCES User(user_id) ON UPDATE CASCADE ON DELETE CASCADE);

load data infile '/var/lib/mysql-files/Group9/reviews.csv' ignore 
    into table Booking
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@listing_id, @id, @date, @reviewer_id, @reviewer_name, @comments)
     set booking_id = @id,
         listing_id = @listing_id,
         guest_id = @reviewer_id,
         booking_date = NULL,
         number_of_people = NULL,
         duration = NULL,
         calculated_price = NULL,
         check_in_date = NULL,
         check_out_date = @date,
         status = 'Checked out';

alter table Booking add constraint Date check(check_in_date<=check_out_date);

SELECT "CREATE TABLE Review" AS " ";
CREATE TABLE Review (
    booking_id int PRIMARY KEY,
    date_of_review date,
    comments varchar(5000),
    FOREIGN KEY (booking_id) REFERENCES Booking(booking_id) ON UPDATE CASCADE ON DELETE CASCADE);

load data infile '/var/lib/mysql-files/Group9/reviews.csv' ignore 
    into table Review
     -- character set latin1
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (@listing_id, @id, @date, @reviewer_id, @reviewer_name, @comments)
        set booking_id = @id,
            date_of_review = @date,
            comments = @comments;