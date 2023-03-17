from bs4 import BeautifulSoup
import requests
url = "https://rule34.xxx/index.php?page=post&s=view&id=6665398"
response = requests.get(url)
# html = r
# soup = BeautifulSoup(html, 'html.parser')




if response.status_code == 200:
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')

  # extract text from all elements with the 'p' tag
  paragraphs = soup.find_all('a')
  for p in paragraphs:
      if "?" in p or "\n" in p:
          print("")
      else:
        text = p.get_text("\n")
        print(text)
    # do something with the text
    # text_to_download = soup.find_all('a', id_='tag-sidebar')
    # for element in text_to_download:
    #     texts = element.get_text(strip="?")
    #     print(texts)
    # do something with the text

    
    
    
else:
  print("Failed to download page from", url)
