import os
import sys
import getopt
import random
import requests
from bs4 import BeautifulSoup as Soup


class M3UWriter(object):
    def __init__(self, write_dir):
        self.cdn_nodes = ['peer1.ustv.to', 'peer2.ustv.to', 'peer3.ustv.to']

        self.channel_codes = ['ABCE', 'A&E', 'AMC', 'APL', 'BBCA', 'BET', 'BOOM', 'BRVO', 'CNE', 'CBSE', 'CMT', 'CNBC',
                              'CNN', 'COM', 'DEST', 'DSC', 'DISE', 'DISJR', 'DXD', 'DIY', 'E!', 'ESPN', 'ESPN2', 'FOOD',
                              'FBN', 'FOXE', 'FNC', 'FS1', 'FS2', 'FREEFM', 'FX', 'FXM', 'FXX', 'GOLF', 'GSN', 'HALL',
                              'HMM', 'HBO', 'HGTV', 'HIST', 'HLN', 'ID', 'LIFE', 'LIFEMOV', 'MLBN', 'MTHD', 'MSNBC',
                              'MTV', 'NGW', 'NGC', 'NBA', 'NBCSN', 'NBCE', 'NFLHD', 'NIKE', 'NKTN', 'OWN', 'OXGN',
                              'PAR', 'PBSE', 'POP', 'SCI', 'SHO', 'STARZ', 'SUND', 'SYFY', 'TBS', 'TCM', 'TELE', 'TNNS',
                              'CWE', 'WEATH', 'TLC', 'TNT', 'TRAV', 'TruTV', 'TVLD', 'UNVSO', 'USA', 'VH1', 'WE']

        self.cdn_channel_codes = ['ABC', 'AE', 'AMC', 'Animal', 'BBCAmerica', 'BET', 'Boomerang', 'Bravo', 'CN', 'CBS',
                                  'CMT', 'CNBC', 'CNN', 'Comedy', 'DA', 'Discovery', 'Disney', 'DisneyJr', 'DisneyXD',
                                  'DIY', 'E', 'ESPN', 'ESPN2', 'FoodNetwork', 'FoxBusiness', 'FOX', 'FoxNews', 'FS1',
                                  'FS2', 'Freeform', 'FX', 'FXMovie', 'FXX', 'GOLF', 'GSN', 'Hallmark', 'HMM', 'HBO',
                                  'HGTV', 'History', 'HLN', 'ID', 'Lifetime', 'LifetimeM', 'MLB', 'MotorTrend', 'MSNBC',
                                  'MTV', 'NatGEOWild', 'NatGEO', 'NBA', 'NBCSN', 'NBC', 'NFL', 'Nickelodeon',
                                  'Nicktoons', 'OWN', 'Oxygen', 'Paramount', 'PBS', 'POP', 'Science', 'Showtime',
                                  'StarZ', 'SundanceTV', 'SYFY', 'TBS', 'TCM', 'Telemundo', 'Tennis', 'CWE',
                                  'https://weather-lh.akamaihd.net/i/twc_1@92006/master.m3u8', 'TLC', 'TNT', 'Travel',
                                  'TruTV', 'TVLand', 'Univision', 'USANetwork', 'VH1', 'WETV']

        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"}
        self.write_dir = write_dir
        self.renew_token_node = 'https://ustvgo.tv/player.php?stream=NFL'
        self.wms_auth_token = {'wmsAuthSign' :'c2VydmVyX3RpbWU9MTAvMTMvMjAyMCAzOjU3OjQ1IFBNJmhhc2hfdmFsdWU9WWVTWThRNDVxWFhZKzFFOGtPMlppUT09JnZhbGlkbWludXRlcz0yNDA='} # Only temporary solution
        self.generated_links = []

    def assemble_hotlink(self, node, channel):
        self.generated_links.append("https://{}/{}/myStream/playlist.m3u8?wmsAuthSign={}".format(
            node, channel, self.wms_auth_token['wmsAuthSign']))

    def generate_links(self):
        print("\nGenerating links...\n")
        for channel in self.cdn_channel_codes:
            if "weather" in channel:
                self.generated_links.append(channel)
            else:
                x = random.randrange(3)
                self.assemble_hotlink(self.cdn_nodes[x], channel)

    def initialize_m3u_file(self):
        if os.path.exists(self.write_dir):
            os.remove(self.write_dir)
            with open(self.write_dir, "w") as writer:
                writer.write('')
                writer.close()
        else:
            with open(self.write_dir, "w") as writer:
                writer.write('')
                writer.close()

    def write_m3u_chunk(self, channel_code, url):
        with open(self.write_dir, "a") as writer:
            writer.write("#EXTM3U\n")
            writer.write("#EXTINF: -1,{}\n".format(channel_code))
            writer.write("#EXTVLCOPT:http-user-agent=\"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 "
                         "Firefox/71.0\"\n")
            writer.write("{}\n\n".format(url))
            writer.close()

    def feed_chunk_writer(self):
        print("\nWriting M3U...\n")
        for code, link in zip(self.channel_codes, self.generated_links):
            self.write_m3u_chunk(code, link)


def main(argv):
    write_dir = ''
    try:
        opts, args = getopt.getopt(argv, "h:o:", ["output="])
    except getopt.GetoptError:
        print('pmg.py -o <outputfile>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('pmg.py -o <outputfile>')
            sys.exit()
        elif opt in ("-o", "--output"):
            write_dir = arg
    if write_dir == '':
        print('pmg.py -o <outputfile>')
        sys.exit()
    mw = M3UWriter(write_dir)
    mw.generate_links()
    mw.initialize_m3u_file()
    mw.feed_chunk_writer()


if __name__ in "__main__":
    main(sys.argv[1:])
