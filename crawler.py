"""
get Shakespeare's Collected Works from http://www.rhymezone.com/r/gwic.cgi?Word=_&Path=shakespeare
store them in specif directory

Author: Bei-Chen Li
"""

import os
import errno
from bs4 import BeautifulSoup
from urllib.request import urlopen

site = 'http://www.rhymezone.com'
# default directory
path = os.path.dirname(os.path.abspath(__file__))


class Crawler(object):
    def __init__(self, path):
        self.site = site
        self.path = path

    def crawl(self):
        """
        get Shakespeare's Collected Works from http://www.rhymezone.com/r/gwic.cgi?Word=_&Path=shakespeare
        store them in specif directory
        """
        all_doc = urlopen(self.site + '/r/gwic.cgi?Word=_&Path=shakespeare')
        soup = BeautifulSoup(all_doc, "html.parser")
        all_dir = self.path + '/shakespeare_collection'
        self.makedir(all_dir)
        genres = soup.find_all('a')[2:6]
        for genre in genres:
            genre_dir = all_dir + '/' + genre.get_text()
            self.makedir(genre_dir)
            genre_site = self.site + genre.get('href')
            soup = BeautifulSoup(urlopen(genre_site), "html.parser")
            works = [work for work in soup.find_all('a') if work.get('href').
                        startswith('/r/gwic.cgi?Word=_&Path=shakespeare/')]
            for work in works:
                work_dir = genre_dir + '/' + work.get_text()
                self.makedir(work_dir)
                work_site = self.site + work.get('href')
                soup = BeautifulSoup(urlopen(work_site), "html.parser")
                scenes = [scene for scene in soup.find_all('a') if scene.get('href').
                            startswith('/r/gwic.cgi?Word=_&Path=shakespeare/'+ str.lower(genre.get_text()) + '/')]
                for scene in scenes:
                    scene_dir = work_dir + '/' + scene.get_text()
                    scene_site = self.site + scene.get('href')
                    soup = BeautifulSoup(urlopen(scene_site), "html.parser")
                    text = soup.find('pre')
                    with open(scene_dir + '.txt', "wt") as out_file:
                        out_file.write(text.get_text())

    def makedir(self, target_path):
        """
        make directory safely at targeting path
        """
        try:
            os.makedirs(target_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
