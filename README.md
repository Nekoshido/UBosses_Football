# UBosses_Football

Football Advanced Statistics.

## How to run using Docker
* Compile Docker container: sudo docker build . -t ubosses_football
* Run container: sudo docker run -P -d -it -v $(pwd):/usr/src/app ubosses_football 

## Scrapping
Scrapping websites to obtain data.

### Squawka
[Squawka](http://www.squawka.com/football-stats/) website uses Opta Sports data. The definitions are [here](http://www.squawka.com/football-stats-definitions)

### WhoScored
[Squawka](https://www.whoscored.com/Statistics) website with players data.

### Transfermarkt
[Transfermarkt](https://www.transfermarkt.com/) website with the value of the players.


