# mma-math-remake
If Fighter A beats Fighter B, and Fighter B beats Fighter C...then Fighter A can beat Fighter C.

This is the law of mma-math.

Merging my love of martial arts and data science, 
this project is a remake of a previous mma-math algorithm I implemented for a data structures and algorithms class. 

The initial mma-math calculator implements a path finding algorithm that finds the shortest path such that a fighter has
a victory over another fighter who has a victory over another fighter such that the path of victories eventually leads 
to the target opponent.


In addition to the path finding algorithm, this remake includes a DASH based GUI that takes in user input and shows 
important statistics and visuals for fighters found in the mma-math path.

# Running the App
Running `app.py` will run the app
```shell script
python app.py
```

# Using the App

### Fighter Input
Fighter input is done through the side bar and include suggestions and automatic validation before running the program.
![validation](assets/gifs/validate.gif)


### Challenger Stats
Upon completion, relevant statistics are shown for input fighters and fighters included on the path. Statistics can be
shown on the fly by clicking the fighter along the path.
![validation](assets/gifs/stats.gif)


### Impossible paths and manually stopping search
In the case that a path isn't found, the program will indicate as such in place of a win path.

Furthermore, certain matchups may take a while to find a path. While the app searches for a path, a timer will indicate 
elapsed time in seconds. The search can be cancelled at any time.
![validation](assets/gifs/cancel.gif)



# Included Files

## Scrapers

`url_scraper.py`: Scraper that retrieves url's containing fighter data


`record_scraper.py`: Scraper that retrieves fight records from a fighters page


## Scripts
`path_finder.py`: Program that runs a modified Dijkstras algorithm to find shortest win path between
 Fighter A and Fighter B
 
 `stat_finder.py`: Program that retrieves a fighters statistics and data to be visualized
 
 `visual.py`: Program that creates graphs and statistical visualizations using fighter data


## Credits and Sources

All images and statistics sourced from ESPN


