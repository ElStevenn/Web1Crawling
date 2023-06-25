import requests
from ImageDownloader import ImageDownloader
import os
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
from pathlib import Path

cls = lambda: os.system('cls')
cls()
path = os.getcwd()
path = Path(path)


def getData():
    url = "https://amazfitwatchfaces.com/mi-band-6/fresh/p/2"
    response = requests.get(url)
    
    # Create a BeatifulSoup object with HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def extract_filename(path):
    """Extract file name from a link. e.j; https://helo/lol.gif to lol.gif"""
    match = re.search(r'([^/]*$)', path)
    if match is not None:
        return match.group(0)
    return None

def extract_extension(filename):
    """Get file extension. e.j: t-rex_m.svg to svg"""
    match = re.search(r'(\.[^.]*$)', filename)
    if match is not None:
        return match.group(0)
    return None

def remove_extension(filename):
    """Remove the extension. e.j: t-rex_m.svg to t-rex_m"""
    return re.sub(r'(\.[^.]*$)', '', filename)

def create_folder(name):
    """Create a folder to put the photos"""
    try:
        os.mkdir(f"{name}_images")
        os.mkdir("CSV_Files")
    except:
        os.rmdir(f"{name}_images")
        os.mkdir(f"{name}_images")
    finally:
        return f"{name}_images"

def remove_spaces_and_create_list(string):
    """Remove all spaces from string and make a list"""
    words = string.split()
    return [word for word in words if word]

def combine_elements(lst):
    """Transform the list and combine the first and second elements. e.j: ['Mi', 'Band', '6', 'ivanssg', '0', '737', '3'] to ['Mi Band', '6', 'ivanssg', '0', '737', '3']"""
    result = []
    combined = ' '.join(lst[:3])
    result.append(combined)
    result.extend(lst[3:])
    return result

def extract_src(html_code):
    """Function to extact src from HTML code"""
    soup = BeautifulSoup(html_code, 'html.parser')
    img_tag = soup.find('img')
    src = img_tag['src']
    return src

def ConvertCSVFile(data):

    """"""
    pass

def main():
    MyLinks = []
    Data = getData()
    folder_name = create_folder("Photos1")
    link_img = Data.find_all('img') # Get image links
    link_div = Data.find_all('div', {'id':'wf-row'})
    print("This is all the data:")

    # Convert HTML in a List
    for all in link_div:
        for wtf in all:  
            Elements = combine_elements(remove_spaces_and_create_list(wtf.text))
            if len(Elements) >= 5:
                DicUserData = {
                    'NAME': Elements[0],
                    'USER': Elements[1],
                    'IMAGE': extract_src(str(wtf)),
                    'STARED': Elements[2],
                    'WATCHED': Elements[3],
                    'DOWNLOADS': Elements[4]
                }
                MyLinks.append(DicUserData)

    DataFrame = pd.DataFrame(MyLinks)  # Convert data to DataFrame
    output_path = path / "CSV_Files" / "output.csv"  # Set the desired output path and filename
    DataFrame.to_csv(output_path, index=False)  # Save the DataFrame as CSV
    
    # Install all the images there are
    """
    for link in tqdm(link_img):
        linkName = extract_filename(link["src"])
        extension = extract_extension(linkName)
        Deflink = remove_extension(linkName)
        MyPath = str(path)+"/"+str(folder_name)
        ImageDownloader("https://amazfitwatchfaces.com/"+str(link["src"]),Deflink, extension=extension, folder_name=MyPath)
    """

if __name__ == '__main__':
    main()