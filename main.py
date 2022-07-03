"""download quran audios from quran central website for different reciters"""

import os
import pyinputplus
import requests

# store the names with the link to first surah (al-fathiha)
namesToLink = {
        "abdul-basit-abd-us-samad" : "https://podcasts.qurancentral.com/abdul-basit/abdul-basit-64-surah-001.mp3",
        "abdur-rahman-as-sudais" : "https://podcasts.qurancentral.com/abdul-rahman-al-sudais/192/abdul-rahman-al-sudais-001-qurancentral.com-192.mp3",
        "ahmad-alnufais" : "https://podcasts.qurancentral.com/ahmad-alnufais/001.mp3",
        }

def main():
    names = list(namesToLink.keys())
    # print(names)

    for i in range(1, len(names)+1):
        print(i, names[i-1])
        
    n = pyinputplus.inputInt("\nSelect the reciter number: ", min=1, max=len(names))
    print(f"Downloading surahs of {names[n-1]}")
    print("Press ctrl-c to quit\n")

    reciter = names[n-1]
    link = namesToLink[reciter]
    surahNumIndex = link.find('001')

    if surahNumIndex == -1:
        print("Unable to find surah number in link")
        exit(1)

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

        print(link)

        # dowloading
        try:
            download = requests.get(link)
        except Exception as error:
            print("Error downloading")
            print(error)
            exit(1)

        # writing to file
        filename = reciter + "/" + link.split('/')[-1]
        with open(filename, "wb") as f:
            f.write(download.content)

    return 0

main()
