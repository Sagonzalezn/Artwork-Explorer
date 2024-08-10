# Artwork Explorer

This is a quick scripting project where you can explore artworks from the  Art Institute of Chicago.

## Description

This app is written in python 3.12.3 and it uses this libraries: 
- json
- requests
- argparse
- reportlab 

It also uses The Art Institute of Chicago's API provides JSON-formatted data as a REST-style service that allows developers to explore and integrate the museum’s public data into their projects. LINK: https://api.artic.edu/docs/#introduction

## Getting Started

### Dependencies


Make sure you have installed the libraries.

The **requirements.txt** file can be used to install them with the following command.

```
pip install -r requirements.txt
```

### Executing program

To run the program execute the following command:
```
python3 artworks.py
```

This will give you a welcome message. The program requires the _-s_ or _--search_ flags followed by a word/term to search for artworks with a related topic.

You can also use the flags:
- -f or --fields: to specify the fields you want to see for the artworks. The fields must be comma separated and without spaces (e.g. title,id,artist_title). By default it shows the tittle of the artwork, the id and the artist. But you can use any of the following: _score, id, image_id, title, artist_title, place_of_origin, short_description, dimensions, medium_display

- -a or --artworks to specify the number of artworks to be displayed. By default it shows 6 artworks and it cannot exceed 15.

When you execute the program, it will display on the terminal the artworks it found and create two files. The first one is a JSON file containing all the information collected from the artworks. The second one is a PDF file with the information.


## Authors

Samuel Gonzalez Nisperuza

## Version History


* 0.1
    * Initial Release



## Acknowledgments

This project was made for an intership task at Endava Bogotá.