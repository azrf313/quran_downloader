"""download quran audios from quran central website for different reciters"""
# store the names with the link to first surah (al-fathiha)
reciters = {
        "abdul-basit-abd-us-samad" : "https://podcasts.qurancentral.com/abdul-basit/abdul-basit-64-surah-001.mp3",
        "abdur-rahman-as-sudais" : "https://podcasts.qurancentral.com/abdul-rahman-al-sudais/192/abdul-rahman-al-sudais-001-qurancentral.com-192.mp3",
        "ahmad-alnufais" : "https://podcasts.qurancentral.com/ahmad-alnufais/001.mp3",
        }




import os
import json
import pyinputplus
import requests


file_surahs = open("surahs.json")
surah_names = json.load(file_surahs)

def error(*msgs):
    print("\n" + "-"*60)
    for msg in msgs:
        print(f"Error: {msg}")
    print("\n" + "-"*60)
    exit(1)

def download_and_save(link, filename, surah_number):
    # dowloading
    try:
        download = requests.get(link)
        if (download.status_code != 200): # error downloading content
            print(f"Error... {surah_names[str(surah_number)]}")
            return False

    # incase of error in downloading
    except Exception as err:
        error("Error downloading", err)
        return False

    # writing to file
    with open(surah_names[str(surah_number)], "wb") as f:
        f.write(download.content)
        print("Done... " + surah_names[str(surah_number)])

    return True

def main():
    total_downloads = 0

    names = list(reciters.keys())

    print("\nPress ctrl-c to quit\n")

    # print all the names
    for i in range(1, len(names)+1):
        print(i, names[i-1])

    # input 
    n = pyinputplus.inputInt("\nSelect the reciter number: ", min=1, max=len(names))
    print(f"Downloading surahs of {names[n-1]}")

    reciter = names[n-1]
    link = reciters[reciter]
    surahNumIndex = link.find('001')

    # incase we cannot find surah number in link
    if surahNumIndex == -1:
        error("Unable to find surah number in link", "Please check your link")

    # create dir for suras
    os.makedirs(reciter, exist_ok=True)

    # generating 114 links
    for i in range(1, 115):
        surah = str(i)
        if (len(surah) == 1):
            surah = '00' + surah
        elif (len(surah) == 2):
            surah = '0' + surah

        old = link[surahNumIndex: surahNumIndex+3]
        link = link.replace(old, surah)
        filename = reciter + "/" + link.split('/')[-1]
        if (download_and_save(link, filename, i) == False):
            continue
        else:
            total_downloads += 1

    print(f"\nDownloaded total of {total_downloads} surahs\n")
    return 0

try:
    main()
except KeyboardInterrupt: # hanling user pressing crtl-c
    print("\nexited by user")
