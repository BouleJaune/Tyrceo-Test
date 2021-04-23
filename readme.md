I had to install with pipwin geopandas and it's dependencies because "Fiona" was apparently unable to install GDAL on my system ... anyway that's what I used :
```
pip install wheel
pip install pipwin

pipwin install numpy
pipwin install pandas
pipwin install shapely
pipwin install gdal
pipwin install fiona
pipwin install pyproj
pipwin install six
pipwin install rtree
pipwin install geopandas
```
For this reason the requirements.txt doesn't contains geopandas and it's dependencies. So either a simple "pip install geopandas" will work for you, or you'll have to do something like I did.



As for the geocoding, there are different APIs but most of the free ones aren't that good. And the free number of requests per day for the good ones is not enough.

I ended up using mapbox geocoding API because I had a token and because I thought that it was what you were using. However it doesn't always yield such good results. 
For example some adresses are like this "multiple appartments in Madrid, example [random postal code]>". In this case it will give us what seem to be random coordinates, whereas the Google geocoding API will at least give us coordinates following the postal code.
For this reason I didn't bother cleaning those outliers since the data in itself is fine and it should be fine with just the right geocoding API, I simply don't have access to a good one. This is why there will be some hotels at random places.

As for the visualisation I am far from being a front-end developper so I used Dash and tried to do something good enough for a test.I hope it will be alright. 
I wanted to do some other stylish things but I would have to learn more about Dash and I'm not so sure that it's the perfect visualisation tool that warrants lots of time to be poured inside.

You just need to run the dashboard.py in the repo root folder to get the dashboard in your localhost (port 8050, it will be written in the console). I also let open the app on my PC and openned the ports to the public. I sent you the IP by mail.
