import requests
from lxml import html
from math import ceil

class letterboxd:
    def __init__(self, username):
        self.profile_url = f'https://letterboxd.com/{username}/'

    
    def get_diary(self, entry=50):
        pages = ceil(entry/50)
    
        # Make an HTTP GET request to fetch diary content
        response = requests.get(self.profile_url+"films/diary/")
        tree = html.fromstring(response.content)

        movie_xpath = '//*[@id="diary-table"]/tbody/tr'
        last_log_cal = []
        diary = []
        for i in range(1, 51):
            raw_movie_det = tree.xpath(movie_xpath+f"[{i}]")[0]

            # get movie and user info
            movie_name = raw_movie_det.xpath("./td[3]/h3/a/text()")
            rel_date = raw_movie_det.xpath("./td[4]/span/text()")
            raw_poster_data = raw_movie_det.xpath("./td[3]/div")[0].attrib
            user_rating = raw_movie_det.xpath("./td[5]/div/span/text()")
            
            # get movie poster
            base_poster_url = "https://a.ltrbxd.com/resized/film-poster"
            # https://a.ltrbxd.com/resized/film-poster/6/3/2/4/4/63244-mankatha-0-35-0-52-crop.jpg?v=a470eb4ca5
            data_film_id = raw_poster_data["data-film-id"]
            data_film_slug = raw_poster_data["data-film-slug"]
            for i in data_film_id:
                base_poster_url += "/"+i
            base_poster_url += "/"+data_film_id
            base_poster_url += "-"+data_film_slug
            base_poster_url += "-0-35-0-52-crop.jpg"

            movie_info = movie_name+rel_date+[base_poster_url]+user_rating

            #get movie log date
            movie_log_cal = raw_movie_det.xpath("./td/div/strong/a/text()")+raw_movie_det.xpath("./td/div/a/small/text()")
            if(len(movie_log_cal)):
                last_log_cal = movie_log_cal
            else:
                movie_log_cal = last_log_cal
            movie_log_date = raw_movie_det.xpath("./td[2]/a/text()")
            formated_date = [movie_log_cal[0]+"/"+movie_log_date[0]+"/"+movie_log_cal[1]]

            # final dict
            diary.append(movie_info+formated_date)
        
        return diary


finalgof = letterboxd("finalgof")
det = finalgof.get_diary()

print(det)