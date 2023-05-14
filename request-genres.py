import requests
import json
import urllib3
import math
import time

# observed from using the website
coarse_genres = {"black"} # TODO: add all genres
cgenres_names= {"black": "Black Metal"} # TODO

results =  {}

for c in coarse_genres:
   cname = cgenres_names[c]
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
         #print(bands[1])
         if bands:
            for b in bands:
                #print(b[2]) #genre
                genres = b[2].replace("(early)", "").replace("(later)", "").replace("(mid)", "")
                genres = genres.split('/')
                for g in genres:
                   if results[c].get(g) is not None:
                      results[c][g] = results[c][g] + 1
                   else:
                      results[c][g] = 1

      else:
         print("status returned: ", page.status_code)
         break

      print("parsed ", offset+500, " bands, of those ", results[c].get(cname), " are basic")
      time.sleep(1)

print(results)
#print('Done!')
