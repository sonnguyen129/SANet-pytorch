import requests,json, os, math, sys

styles = ["impressionismus",
"realismus",
"romantik",
"expressionismus",
"post-impressionismus",
"surrealismus",
"art-nouveau-modern",
"barock",
"symbolismus",
"abstrakter-expressionismus",
"naive-kunst-primitivismus",
"neoklassizistismus",
"rokkoko",
"nordliche-renaissance",
"kubismus",
"minimalismus",
"pop-art",
"informel",
"abstrakte-kunst",
"farbfeldmalerei",
"ukiyo-e",
"manierismus-spatrenaissance",
"hochrenaissance",
"fruhrenaissance",
"konzeptuelle-kunst",
"magischer-realismus",
"neoexpressionismus",
"op-art"]

def print_progress(a):
    sys.stdout.write('\r')
    sys.stdout.write( a )
    sys.stdout.flush()

#gets the data for one page and style
def getData(style, page):
    url = 'https://www.wikiart.org/en/paintings-by-style/'+style
    data = {'json' : 2, 'page' : page }
    res = requests.post(url, data)
   
    while res.status_code != 200:
         res = requests.post(url, data)
    out = json.loads(res.text)
    
    
    return out

#gets all data for one style
def getAllPaintings(style):
    print("\ngettings {} paintings".format(style))
    init = getData(style,1)
    numPaintings = init['AllPaintingsCount']
    pages = math.ceil(numPaintings / init['PageSize']) + 1 
    
    paintings = init['Paintings']  
    for i in range(2, pages):
        if i % 40: 
            print_progress("{}%".format(round((i/pages)*100,2)))
        pageData = getData(style, i)['Paintings']
        while (len(pageData) < 60) and (i < pages-1):
            print("redo"+str(i))
            pageData = getData(style, i)['Paintings']
        paintings = paintings + pageData
    if not (numPaintings == len(paintings)):
        raise Exception("More pictures expected")
    return paintings



rootFolder = os.path.expanduser("~/wikiartData/")
stylesToDownload = styles[:1]

#multiple connections would speed this up, puts more stress on the server though
data = {}
for style in stylesToDownload:
    data[style] = getAllPaintings(style)

"""note that some pictures are inproperly named and have the jpg extention. 
This will cause problems on programms that rely on the extention. It is possible to check with import imghdr
imghdr.what() and rename the file accordingly.

This method is also not efficient at all, best would be to have multiple threads that connect 
and get the data, then write the files in another thread"""


for style in data:
    print("\nprocessing style '{}'".format(style))
    folder = rootFolder+style+'/'
    
    try:
        os.makedirs(folder)
    except FileExistsError:
        print("writing to existing folder")
    
    for i, metaData in enumerate(data[style]):
        if i%20 == 0:
            print_progress("{}%".format(round(i/len(data[style])*100,2)))
        
        fullPath = folder+os.path.basename(metaData['image'])
        
        #only make the request and save the file if the file does not exist
        if not os.path.isfile(fullPath):
            response = requests.get(metaData['image'])
            while response.status_code != 200:
                response = requests.get(metaData['image'])

            with open(fullPath, 'wb') as f:
                f.write(response.content)
