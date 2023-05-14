import requests
#import json
import urllib3
import math
import time
import re

# observed from using the website
coarse_genres = {
   "black", "death", "doom",
   "electronic", "avantgarde", "folk",
   "gothic", "grind", "groove",
   "heavy", "metalcore", "power",
   "prog", "speed", "orchestral",
   "thrash"
}

results =  {}

for c in coarse_genres:
   url = "https://www.metal-archives.com/browse/ajax-genre/g/"+c+"/json/1"

   results[c] = {}

   headers =  {
      "Accept": "application/json",
      "User-Agent": "metal-is-love",
      "Accept-Encoding": urllib3.util.SKIP_HEADER
   }
   params = { "sEcho": "test" }
   pre = requests.get(url, params=params, headers=headers)
   total = pre.json().get("iTotalDisplayRecords")
   max = math.ceil(total / 500)

   for i in range(0, max):
      offset = i * 500
      params = { "iDisplayStart": offset, "sEcho": 0}

      page = requests.get(url, params=params, headers=headers)

      if page.status_code == 200:
         bands = page.json().get("aaData")
         if bands:
            for b in bands:
                genres = b[2].replace("(early)", "").replace("(early", "").replace("early)", "")
                genres = genres.replace("(mid)", "").replace("(mid", "").replace("mid)", "")
                genres = genres.replace("(later)", "").replace("(later", "").replace("later)", "")
                genres = re.split('[/,;]', genres)
                for g in genres:
                   if results[c].get(g) is not None:
                      results[c][g] = results[c][g] + 1
                   else:
                      results[c][g] = 1

      else:
         print("status returned: ", page.status_code)
         break

      #print("[", c, "]: parsed ", offset+500, " bands and ", len(results[c]), " associated genres found")
      time.sleep(1)

print(results)
