from bs4 import BeautifulSoup
import tkinter as tk

import requests

def log(message):
    outbox_box.insert(tk.END, message + "\n")


def crawl_run():
    url = "http://citelms.net/Internships/Summer_2018/Fan_Site/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises an error for bad responses

    link_query = []
    Visited_Links = []
    dictionary = {}
    soup = BeautifulSoup(response.text, "html.parser")


    

# create the soup which is an xml tree of the page

    title_tag = soup.find("title")
    log("Title with html:" + str(title_tag))
    log("Title text: " + title_tag.text)

# Find all <a> links
    link_query.append(url + "index.html")

    while len(link_query):
        link = link_query.pop(0)
        if link in Visited_Links:
            continue
    
        response = requests.get(link, timeout=10)
        response.raise_for_status()  # Raises an error for bad responses
        
        soup = BeautifulSoup(response.text, "html.parser")

        Visited_Links.append(link)

        # word counter 
        text = soup.get_text()
        text = text.lower()

        words = text.split()

        word_count = {}

        for w in words:
            clean = ""
            for ch in w:
                if "a" <= ch <= "z":
                    clean += ch
            if len(clean) <= 2:
                continue

            if clean not in word_count:
                word_count[clean] = 1
            else: 
                word_count[clean] += 1
        
        sorted_words = sorted(word_count, key=word_count.get, reverse=True)
        
        top_words = sorted_words[:10]

        for w in top_words:
            dictionary[w] = link 
            log("Saved word:" + w)


    
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.text.strip().lower()
            dictionary[title] = link 
            log("Page Title:" + title)
    
        tags = soup.find_all("a")
        for tag in tags: 
        #tag.get("href")
            href = tag.get("href")
            if href:
                if href.endswith("html"):
                    if "http" not in href:
                        if "void" not in href and "pdf" not in href and "javascript" not in href:
                            full_url = url + href
                            log("Adding:" + full_url)
                            link_query.append(full_url)

    query = search_entry.get().lower()

    if query in dictionary:
        log("Found:" + dictionary[query])
    else:
        log("Not found.")

    


root = tk.Tk()
root.title("Web Crawler")
root.geometry("500x400")
root.configure(bg="yellow")

label = tk.Label(root, text="Click button to crawl", bg="yellow")
label.pack(pady=10)

search_entry = tk.Entry(root,width=40)
search_entry.pack(pady=5)

crawl_button = tk.Button(root, text="Run Crawler", command=crawl_run)
crawl_button.pack(pady=10)

outbox_box = tk.Text(root, height=20, width=60)
outbox_box.pack(pady=10)

root.mainloop()