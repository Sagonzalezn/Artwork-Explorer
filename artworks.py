import json
import requests
import argparse
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter

url = "https://api.artic.edu/api/v1/artworks/search"

parser = argparse.ArgumentParser(description='Artwork explorer from AIC')

parser.add_argument("-s", "--search", type=str, help="Finds artworks related to passed argument")
parser.add_argument("-f", "--fields", type=str, default= 'title,id,artist_title', help="Displays selected fields of searched artworks (Must be comma separated, no spaces, e.g. title,author,description)")
parser.add_argument("-a", "--artworks", type=int, default=6, choices=(1,16), help="Number of artworks to be displayed (Default=6, , must be between 1 and 15)")

args = parser.parse_args()

if args.search == None and args.fields == 'title,id,artist_title' and args.artworks == 6:
    print("\nWelcome to Art Intitute of Chicago art explorer!\n\n   ---> Run again with '--search' or '-s' to find artworks\n\n" + 
          "Posible fields are:\n\n[_score, id, image_id, title, artist_title, place_of_origin, short_description, dimensions, medium_display]\n\n")
    exit()

selected = args.fields.split(',')

#Request Data
response = requests.get(url,params={
    'q' : args.search,
    'page' : 1,
    'limit' : args.artworks,
    'fields' : args.fields
})


#Create JSON
if response.status_code == 200:
    response_json = response.json()
    with open('response.json', 'w') as f:
        json.dump(response_json, f)
else:
    print("Error creating json")


artworklist = []

#Display result
if 'data' in response_json:
    artworks = response_json['data']
    print('\n --> Here are ' + str(args.artworks) + ' artworks related to ' + args.search + '\n')
    print('------------------------------------\n')
    for artwork in artworks:

        artworkinfo = {}
        for field in selected:

            artworkinfo[field] = artwork.get(field, 'N/A')
            print('* ' + str(field).capitalize() + ': ' +str(artwork.get(field, 'N/A')) + '\n')
        print('------------------------------------\n')

        artworklist.append(artworkinfo)
else:
    print("Error displaying fields")


#Create PDF
fileName = 'response.pdf'
documentTitle = 'Art Institute of Chicago'
title = str(args.artworks) + ' artworks related to ' + args.search
subTitle = 'Art Insitute of Chicago'
textLines = [
    'Author: ' + '',
    'Description',
]
image = 'image.jpg'




# creating a pdf object 
pdf = canvas.Canvas(fileName, pagesize=letter) 
width, height = letter
  
# setting the title of the document 
pdf.setTitle(documentTitle) 

# registering a external font in python 
pdfmetrics.registerFont( 
    TTFont('Vera', 'Vera.ttf') 
) 
  
# creating the title by setting it's font  
# and putting it on the canvas 
pdf.setFont('Vera', 36) 
pdf.drawCentredString(width / 2, height - 50, title)

current_y = height - 100


#CHECK FOR SPACE IN PDF OR CREATE NEW PAGE
def check_and_add_page():
    global current_y
    if current_y < 100:  # Check if there's less than 100 points of space remaining
        pdf.showPage()  # Create a new page
        pdf.setFont('Vera', 36)
        pdf.drawCentredString(width / 2, height - 50, title)
        current_y = height - 100


for i, artwork in enumerate(artworklist):
    check_and_add_page()

    # Define subtitle for each artwork
    subtitle = f"Artwork {i + 1}"
    
    # Set subtitle font and color
    pdf.setFillColorRGB(0, 0, 255)
    pdf.setFont("Vera", 24)
    pdf.drawCentredString(width / 2, current_y, subtitle)
    
    # Draw a line below the subtitle
    pdf.line(30, current_y - 10, width - 30, current_y - 10)
    
    # Create multiline text
    text = pdf.beginText(40, current_y - 40)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    
    # Add artwork details to text
    for field, value in artwork.items():
        text.textLine(f"{field.capitalize()}: {value}")
    
    pdf.drawText(text)
    
    # Adjust the vertical position for the next artwork
    current_y -= 150  # Adjust this value to add spacing between artworks
    
    
    # Add a line separating each artwork
    pdf.line(30, current_y - 10, width - 30, current_y - 10)

#pdf.drawInlineImage(image, 130, 150) 

pdf.save()
