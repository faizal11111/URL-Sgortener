# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata
from datetime import datetime
class URLMapping:
    def __init__(self):
        self.url_map = {}
        self.click_count = {}
        self.creation_time = {}

    def add_url(self, short_code, original_url):
        self.url_map[short_code] = original_url
        self.click_count[short_code] = 0
        self.creation_time[short_code] = datetime.now()

    def get_original_url(self, short_code):
        return self.url_map.get(short_code)

    def increment_click_count(self, short_code):
        if short_code in self.click_count:
            self.click_count[short_code] += 1

    def get_click_count(self, short_code):
        return self.click_count.get(short_code, 0)

    def get_creation_time(self, short_code):
        return self.creation_time.get(short_code)
