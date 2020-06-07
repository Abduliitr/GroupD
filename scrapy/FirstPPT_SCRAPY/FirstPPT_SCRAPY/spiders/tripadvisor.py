# -*- coding: utf-8 -*-
import scrapy


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    # allowed_domains = ['https://www.tripadvisor.in/Hotel_Review-g303877-d1797775-Reviews-The_Crown_Goa-Panjim_North_Goa_District_Goa.html']
    # start_urls = ['https://www.tripadvisor.in/Hotel_Review-g303877-d1797775-Reviews-or5-The_Crown_Goa-Panjim_North_Goa_District_Goa.html#REVIEWS']
    # start_urls= ['https://www.tripadvisor.in/Hotel_Review-g15149265-d2041908-Reviews-or5-Mayfair_Hideaway_Spa_Resort-Quitol_Canaguinim_South_Goa_District_Goa.html#REVIEWS']
    # start_urls=['https://www.tripadvisor.in/Hotel_Review-g306995-d2396935-Reviews-or5-Casa_de_Cajino-Calangute_North_Goa_District_Goa.html#REVIEWS']
    # start_urls=['https://www.tripadvisor.in/Hotel_Review-g303877-d1480400-Reviews-or5-Vivanta_Goa_Panaji-Panjim_North_Goa_District_Goa.html#REVIEWS']
    # start_urls=['https://www.tripadvisor.in/Hotel_Review-g297605-d2057388-Reviews-or5-Country_Inn_Suites_by_Radisson_Goa_Candolim-Candolim_Bardez_North_Goa_District_Goa.html#REVIEWS']
    # start_urls = ['https://www.tripadvisor.in/Hotel_Review-g297605-d9452306-Reviews-or5-Hyatt_Centric_Candolim_Goa-Candolim_Bardez_North_Goa_District_Goa.html#REVIEWS']
    start_urls = [
        'https://www.tripadvisor.in/Hotels-g12412660-North_Goa_District_Goa-Hotels.html']

    def parse(self, response):
        links = response.xpath(
            '//a[@class="property_title prominent "]/@href').extract()

        for link in links:
            request = scrapy.Request(
                'https://www.tripadvisor.in'+link, callback=self.parse_review)
            yield request 
            next_page_url = response.xpath(
            '//a[@class="nav next ui_button primary"]/@href').extract_first()
        if next_page_url:
            absolute_next_page_url = 'https://www.tripadvisor.in'+next_page_url
            PR = scrapy.Request(
                absolute_next_page_url,
                dont_filter=True,
                callback=self.parse
            )
            yield PR

    def parse_review(self, response):
        # Comment=response.xpath('//*[@class="location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"]/span/text()').extract()
        # yield {'Comment':Comment}
        # parent=response.xpath('//*[@data-test-target="reviews-tab"]').get()
        # comments=parent.xpath('.//*[@class="hotels-community-tab-common-Card__card--ihfZB"]')
        comments = response.xpath(
            '//*[@data-test-target="reviews-tab"]//div[contains(@class,"hotels-community-tab-common-Card__card--ihfZB")]')
        for comment in comments:
            comment_name = comment.xpath(
                './/*[@class="social-member-event-MemberEventOnObjectBlock__event_type--3njyv"]/span/a/text()').extract_first()
            comment_location = comment.xpath(
                './/*[@class="social-member-MemberHeaderStats__event_info--30wFs"]/span/span/text()').extract_first()
            comment_text = comment.xpath(
                './/*[@class="location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"]/span/text()').get()
            comment_date = comment.xpath(
                './/*[@class="location-review-review-list-parts-EventDate__event_date--1epHa"]/text()').extract_first()
            comment_typ = comment.xpath(
                './/*[@class="location-review-review-list-parts-TripType__trip_type--3w17i"]/text()').extract_first()
            # comment_typ=comment.xpath('.//*[@class="hotels-community-tab-reviews-ReviewsTabContent__footer--2FHIK"]').get()
            comment_rating_excellent = len(comment.xpath(
                './/*[@class="ui_bubble_rating bubble_50"]'))
            comment_rating_Very_good = len(comment.xpath(
                './/*[@class="ui_bubble_rating bubble_40"]'))
            comment_rating_average = len(comment.xpath(
                './/*[@class="ui_bubble_rating bubble_30"]'))
            comment_rating_poor = len(comment.xpath(
                './/*[@class="ui_bubble_rating bubble_20"]'))
            comment_rating_terrible = len(comment.xpath(
                './/*[@class="ui_bubble_rating bubble_10"]'))
            hotel_name = response.xpath(
                '//*[@id="HEADING"]/text()').extract_first()

            comment_rating = ""
            if comment_rating_excellent == 1:
                comment_rating = "EXCELLENT"
            elif comment_rating_Very_good == 1:
                comment_rating = "VERY GOOD"
            elif comment_rating_average == 1:
                comment_rating = "AVERAGE"
            elif comment_rating_poor == 1 or comment_rating_terrible == 1:
                comment_rating = "POOR"

            if comment_location == " contribution" or comment_location == " contributions":
                comment_location = "NULL"
            yield{'Hotel_name': hotel_name, 'Name': comment_name, 'Location': comment_location, 'comment': comment_text, 'date': comment_date, 'type': comment_typ, 'Rating': comment_rating}

        # next_page_url=response.xpath('//*[@class="location-review-pagination-card-PaginationCard__wrapper--3epz_"]/div/a/@href').extract_first()
        # next_page_url = response.xpath(
        #     '//*[@class="location-review-pagination-card-PaginationCard__wrapper--3epz_"]/div/a/@href')[1].extract()
        next_page_url = response.xpath(
            '//a[@class="ui_button nav next primary "]/@href').extract_first()
        if next_page_url:
            absolute_next_page_url = 'https://www.tripadvisor.in'+next_page_url
            PR = scrapy.Request(
                absolute_next_page_url,
                dont_filter=True,
                callback=self.parse_review
            )
            yield PR
