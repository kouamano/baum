#!/usr/env python
#-*- coding:utf-8 -*-
import os
import extract,freq

# コマンド実行時に最初に実行されるメソッド
def cmd(args,options={}):
  dirpath = options.inputs
  number = int(options.n)
  list = os.listdir(dirpath)
  result = {}
  phrases = []


  # すべてのファイルに対して集計処理を行う
  for filename in list:
    # 本文の抽出
    content = extract.extract(os.path.join(dirpath,filename))
    # フレーズの抽出と集計
    for sentence in content['body']:
      phrases += map((lambda x: " ".join(x)),extract.make_phrase(sentence,number))

  result = freq.freq_tally(phrases).items()

  # 集計結果を出力する
  return result

if __name__ == "__main__":
  import sys
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-i", "--input", dest="inputs",
                    help="read xmlfiles in DIRECTORY as journal documents",
                    metavar="DIRECTORY")
  parser.add_option("-n", "--numterms", dest="n",
                    help="set number of terms",
                    metavar="NUMBER")
  parser.add_option("-t", "--threshold", dest="t",
                    help="set threshold of counting",
                    metavar="THRESHOLD")

  (options, args) = parser.parse_args()
  result = sorted(cmd(args, options=options), key=lambda x:int(x[1]), reverse=True)

  threshold = int(options.t)

  for item in result:
    if item[1]>=threshold:
      print item[0]+" : "+str(item[1])
