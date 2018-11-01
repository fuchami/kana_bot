#-*- encoding:utf-8 -*-

from requests_oauthlib import OAuth1Session
import requests
import json
import sys, os, re
import MeCab
import random

#token = None
my_name = None

#Mecabによってわかちがきを行う
def wakati(text):
    #余計な文字列を除去
    
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('#kana_nishino', "", text)
    text=re.sub('/', "", text  )
    text=re.sub('#西野カナ', "", text)
    
    
    t = MeCab.Tagger("-Owakati")
    m = t.parse(text)
    result = m.rstrip(" \n").split(" ")
    
    return result

#連鎖数3のマルコフ連鎖にて文章生成
def create_tw(wordlist):
    markov = {}
    w1 = ""
    w2 = ""
    w3 = ""
    endword = ["。", "!", "？"]
    space = "_"
    
    for word in wordlist:
        if w1 and w2 and w3:
            if(w1, w2, w3) not in markov:
                markov[(w1, w2, w3)] = []
            markov[(w1, w2, w3)].append(word)
        w1, w2, w3 = w2, w3, word
        
        
    count = 0
    sentence = ""
    w1, w2, w3 = random.choice(markov.keys())
    while count < len(wordlist):
        tmp = random.choice(markov[w1, w2, w3])
        #句読点などの区切りがついたら文章作成を終了
        if tmp in endword:
            break
        sentence += tmp
        w1, w2, w3 = w2, w3, tmp
        count += 1
        if count > 20:
            break
            
    return sentence

#main関数
def main():
    CK = ''                             
    CS = ''         
    AT = '' 
    AS = ''
    
    
    filename = "data.txt"
    src = open(filename, "r").read()

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"
    #わかち書き
    wordlist = wakati(src)
    
    #文の作成
    tw = create_tw(wordlist)
    # ツイート本文
    params = {"status": tw}

    # OAuth認証で POST method で投稿
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.post(url, params = params)

    # レスポンスを確認
    if req.status_code == 200:
        print ("posted tweet:" + tw)
    else:
        print ("Error: %d" % req.status_code)    
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
    



