#-*- encoding:utf-8 -*-
"""
西野カナの歌詞botから収集

""""

import requests_oauthlib
import requests
import json
import sys, os, re
import MeCab
import random

#ツイートの取得
def get_tw(account):
    session = requests_oauthlib.OAuth1Session(
        "", #Consumer Key
        "", #Consumer Secret
        "", #Access Token
        "" #Access Token Secret    
    )
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    
    res = session.get(url, params = {'screen_name': account, 'count':200,'include_rts':False})
    
    maxid = 0
    i = 0
    f = open("data.txt", "a")
    
    #ツイートを取得
    while True:
        res_text = json.loads(res.text)
        for r in res_text:
            if maxid > r['id'] or maxid == 0:
                maxid = r['id']
            tw = r['text'].encode('utf-8')
            f.write(tw)
            i = i +1
        if  500<= i:
            break
        res =  session.get(url, params = {'screen_name': account, 'count':200,'include_rts':False, 'max_id': r['id']-1})
        

    #APIの呼び出し・ステータスコード判定
    #200が正常終了である
    if res.status_code != 200:
        #正常終了しなければエラー表示
        print ("Twitter API Error: %d" % res.status_code)
        sys.exit(1)
        
    f.close()
    
    return 0

#main関数
def main():
    
    #ツイートを取得する
    get_tw("kanayan_lyrics")
    get_tw("kana_lyrics")
    print("ツイートを収集しました")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
    



