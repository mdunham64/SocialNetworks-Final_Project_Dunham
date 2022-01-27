import json
import csv
import numpy as np
from matplotlib import pyplot as plt


class Video:

    def __init__(self, Collector_item):
        self.nickname = Collector_item['authorMeta']['nickName']
        self.name = Collector_item['authorMeta']['name']
        self.secUid = Collector_item['authorMeta']['secUid']
        self.verified = Collector_item['authorMeta']['verified']
        self.commentCount = Collector_item['commentCount']
        self.createTime = Collector_item['createTime']
        self.likes = Collector_item['diggCount']
        hashtags = []
        for hashtag in Collector_item['hashtags']:
            hashtags.append(hashtag['name'])
        self.hashtags = hashtags
        self.mentions = Collector_item['mentions']
        self.musicAuthor = Collector_item['musicMeta']['musicAuthor']
        self.musicName = Collector_item['musicMeta']['musicName']
        self.musicOriginal = Collector_item['musicMeta']['musicOriginal']
        self.playcount = Collector_item['playCount']
        self.sharecount = Collector_item['shareCount']
        self.videotext = Collector_item['text']
        self.videolength = Collector_item['videoMeta']['duration']


def plot_numberofhashtags_vs_playcount(video_list):
    view_list = []
    hashtag_count = []
    for video in video_list:
        view_list.append(video.playcount)
        hashtag_count.append(len(video.hashtags))
    x = view_list
    y = hashtag_count
    plt.title('Views vs. Number of Hashtags in Video')
    plt.xlabel('Video Views')
    plt.ylabel('Number of Hashtags')
    plt.plot(x, y, "ob")
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-o")
    plt.savefig("views_vs_hashtags")
    plt.show()


def plot_sharecount_vs_playcount(video_list):
    view_list = []
    sharecount_list = []
    for video in video_list:
        view_list.append(video.playcount)
        sharecount_list.append(video.sharecount)
    x = view_list
    y = sharecount_list
    plt.title('Views vs. Shares')
    plt.xlabel('Video Views')
    plt.ylabel('Video Shares')
    plt.plot(x, y, "ob")
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-o")
    plt.savefig("views_vs_shares")
    plt.show()


def plot_numberofcomments_vs_playcount(video_list):
    view_list = []
    numofcomments = []
    for video in video_list:
        view_list.append(video.playcount)
        numofcomments.append(video.commentCount)
    x = view_list
    y = numofcomments
    plt.title('Views vs. Comments')
    plt.xlabel('Video Views')
    plt.ylabel('Video Comments')
    plt.plot(x, y, "ob")
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-o")
    plt.savefig("views_vs_comments")
    plt.show()


def plot_videolength_vs_playcount(video_list):
    view_list = []
    video_length = []
    for video in video_list:
        view_list.append(video.playcount)
        video_length.append(video.videolength)
    x = view_list
    y = video_length
    plt.title('Views vs. Length of Video')
    plt.xlabel('Video Views')
    plt.ylabel('Video Length')
    plt.plot(x, y, "ob")
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r-o")
    plt.savefig("views_vs_videolength")
    plt.show()


if __name__ == '__main__':

    #  this is preprocessing and importing the json file
    file = open('trending.json', encoding='utf8')
    raw_data = json.load(file)
    file.close()
    trending_video_list = raw_data[
        'collector']  # the video meta data in the json file are seated under this collector object
    #  this loop changes the unorganized json file into objects with easy variables for ease of processing
    all_video_objs = []
    for video in trending_video_list:
        temp_video = Video(video)

    #  below are example plots I created and will be referencing in my paper/presentation
    plot_numberofhashtags_vs_playcount(all_video_objs)
    plot_sharecount_vs_playcount(all_video_objs)
    plot_numberofcomments_vs_playcount(all_video_objs)
    plot_videolength_vs_playcount(all_video_objs)

    #  here I wanted to determine the amount of verified accounts in the top 1000 vs not verified
    verified_counter = 0
    non_verified_counter = 0
    for video in all_video_objs:
        if video.verified:
            verified_counter += 1
        else:
            non_verified_counter += 1

    f = open('tiktoks_trending.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    print(trending_video_list[4]['hashtags'])
    for video in trending_video_list:
        row = [video['authorMeta']['nickName'], video['authorMeta']['name'], video['text'],
               video['videoMeta']['duration'], video['musicMeta']['musicAuthor'], video['musicMeta']['musicName']]
        writer.writerow(row)

    f.close()
    print(f"number of verified creators in the top 1000 of trending: {verified_counter} \n"
          f"number of non-verified creators in the top 1000 of trending: {non_verified_counter}")
