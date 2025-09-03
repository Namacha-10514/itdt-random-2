import copy
import discord
import json
import random
import requests
import time
import os

from keep_alive import HealthCheckServer

from datetime import datetime
from datetime import timedelta
from discord import Option
from discord.ext import tasks
from zoneinfo import ZoneInfo

intents = discord.Intents.default()
intents.members = True

db_url    = "https://script.google.com/macros/s/AKfycbzNnzDMS2srhdu0oz7zt7rux7ZZCD3q5D3XKwesEhzjvJlhePu7qBMv_QjesdAynv40/exec"
db_url_sl = "https://script.google.com/macros/s/AKfycbxpDx-9KkQhuFHDbmfR75XtUFHrN_eRWh5PoM_n4mLbNuBrddwfcrkxA7WNcPg2b8_MLA/exec"
db_url_lg = "https://script.google.com/macros/s/AKfycbw5CkdE-CoDZxDH7SJjLz0Pf4HuRU25b5uUOmcoOaPtRfwWu8-MdksWDTZuWApprCTQ/exec"
db_url_st = "https://script.google.com/macros/s/AKfycbw-KA9EsIdYidNePnDzWYbsvpbDwSti3jRvJb0uhU7CZDJBzb229rGFxM1zmMRxKOC6sg/exec"
db_url_ds = "https://script.google.com/macros/s/AKfycbzmVpf5zK-_pBuEzG2akC3JjcSJzlGvlTWtmTiBRUQLRCu14Tt3uC-ceU6MsfvFOcbWpg/exec"

db_url_tm = "https://script.google.com/macros/s/AKfycbyJTVJVjMsmIjA1W9LUEJBjx6myDFPZ0qspUtp57DRavT_0ZVzkewQyx2V4FSI1rAYJ/exec"

db_url_hd = "https://script.google.com/macros/s/AKfycbwxl8D7wKT341-3ZsQJ1XimVuHQRlYm9knjdqzR5YXdDpG4xjtVdOYGNst-yPMFN-za/exec"
db_url_ez = "https://script.google.com/macros/s/AKfycbxqsf6jTaRKbFtCIncHij2K0R-c9oysd2hJ-VtxJuqT_llTslKFtfeza0h5nQO1TBhz0Q/exec"
db_url_sg = "https://script.google.com/macros/s/AKfycbxZSWT3rRWNagfY24wzG6x8DKORCe6hHeTd_q1BLzNemUTAUNywEhJ-wOGqEDQVvN8/exec"
db_url_nds = "https://script.google.com/macros/s/AKfycby5ky6cdhVu_Gf-MJKa7TeAh54I0dMiV1kBPCmwGS98xiCVASBRBp1QwgCT49YxxJ8osQ/exec"
db_url_psp = "https://script.google.com/macros/s/AKfycbxPDXopemBFbDnsjljAtjse5IzbPDF72M6guAPaFEgpfW5IKdXgGDQ1VrAK7nLCBIQRQw/exec"
db_url_pk = "https://script.google.com/macros/s/AKfycbxDJWN5R1OagCq-8Mh6uXLLNFrlJyJMFIOx8kn3qjmEEQe3zCEVq2Hn6VZmM_1AFovenQ/exec"

db_url_dp = "https://script.google.com/macros/s/AKfycbx1495yVN50lyffmhaDx69jDma8H43HC-lQGf-aSRQK4ljMIAo9ywACP82xHtTMXVQ/exec"

file_kj = open('kanji.json', 'r')

res = requests.get(db_url)
res_sl = requests.get(db_url_sl)
res_lg = requests.get(db_url_lg)
res_st = requests.get(db_url_st)
res_ds = requests.get(db_url_ds)
res_tm = requests.get(db_url_tm)

res_hd = requests.get(db_url_hd)
res_ez = requests.get(db_url_ez)
res_sg = requests.get(db_url_sg)
res_nds = requests.get(db_url_nds)
res_psp = requests.get(db_url_psp)
res_pk = requests.get(db_url_pk)

res_dp = requests.get(db_url_dp)

res_kj = file_kj.read()

song_db = json.loads(res.text)
song_db_sl = json.loads(res_sl.text)
song_db_lg = json.loads(res_lg.text)
song_db_st = json.loads(res_st.text)
song_db_ds = json.loads(res_ds.text)
song_db_hd = json.loads(res_hd.text)
song_db_tm = json.loads(res_tm.text)
song_db_ez = json.loads(res_ez.text)
song_db_sg = json.loads(res_sg.text)
song_db_nds = json.loads(res_nds.text)
song_db_psp = json.loads(res_psp.text)
song_db_pk = json.loads(res_pk.text)

song_db_dp = json.loads(res_dp.text)

kanji_db = json.loads(res_kj)

TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot(intents=intents)

all_levels = [
  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
  "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "41",
  "99", "???", "(^^)", "∞", "NaN"
]

all_levels_dp = [
  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13",
  "14", "15", "99", "???", "Φ"
]

all_random_options = [
  "PlaySpeed(Easy)", "Reg.Speed", "PlaySpeed", "JudgeRange",
  "JudgeRange(S-Random)", "PlaySpeed(Hard)", "JudgeRange(Hard)"
]

all_tournament = ["9_220723", "9_220723_final"]

dan_level = {
  "ビギナー": [0, 0, 0, 1],
  "初段": [1, 1, 2, 2],
  "二段": [3, 4, 4, 4],
  "三段": [5, 5, 5, 6],
  "四段": [7, 7, 8, 8],
  "五段": [9, 9, 9, 9],
  "六段": [10, 10, 10, 11],
  "七段": [11, 12, 12, 13],
  "八段": [13, 13, 14, 14],
  "九段": [15, 15, 16, 16],
  "十段": [17, 17, 17, 18],
  "皆伝": [19, 19, 19, 20],
  "Overjoy": [20, 20, 20, 21],
  "Undefined": [21, 22, 23, 24],
  "Unplayable": [99, 99, 99, 99],
  "Thinking": [101, 101, 101, 101]
}

options = [[
  "Normal", "x2 Scroll", "Doron", "Turn", "RedOnly", "BlueOnly",
  "PlaySpeed(Easy)"
], [
  "x3 Scroll", "Shuffle", "G.Judge H", "Reg.Speed", "PlaySpeed", "JudgeRange"
], ["x4 Scroll", "Stealth", "JudgeRange(Hard)"],
           ["G.Judge A", "PlaySpeed(Hard)"]]

ai_chan = [
  "もちろんです！{1}の「{0}2」っていう曲はめっちゃオススメですよ！\nグループ感が強く、野性味あふれるリズムに合わせて反応しなければならないため、スピード感あるプレイが求められます。\nしかし、慣れるとその高揚感を味わえる楽曲です。",
  "なら、「{0}」by {1}は聴いているだけで元気になれますよ。\n軽快なサウンドと洗練された難易度が魅力です。\n音量上げて大きく指を踊らせてみてください！",
  "「{0}」は歌詞が印象的で、{1}の歌声も本当に素晴らしいです。\n速くテンポの良い曲調で、エネルギッシュなプレイを求められます。\n盛り上がりたいときにおすすめですよ！\nぜひ挑戦してみてください。",
  "はい、「{0}」もオススメです！\n古典的なフレーズから始まり、徐々にメロディが膨らんでいきます。\nさらに、サビのリズムは非常に刺激的です。\nミスをしないように集中力を切らさず挑戦してみてください！\nきっと他の楽曲よりワクワクするかもしれませんよ！",
  "はい、もちろんです！\n「{0}」by {1} は、切なく儚いメロディーが印象的な楽曲です。\n指の動きの繊細さと正確さが求められます。\n難易度はやや高めですが心に残る曲だと思います。\n是非チャレンジしてみてください！",
  "了解です！\n「{0}」by {1}は、美しい女性ボーカルが印象的な楽曲です。\n軽快なリズムに乗って指を滑らせる快感があり、難易度もちょうどよく初心者におすすめです。\nレベルアップしたい方は、フルコンボ目指して挑戦してみてください！",
  "「{0}」がオススメです！\n華やかな曲調で、テンポが良いので気持ちよくプレイできます。\nMVもカラフルで、爽快感ある演出に心が躍ります。\n是非チャレンジしてみてください！",
  "「{0}」by {1}は、キャッチーなメロディーが鮮やかに印象に残ります。\nリズミカルなビートが心地よく、手軽に楽しくプレイできる曲の一つです。\n始めたばかりの初心者の方でも、気楽に楽しめると思います！",
  "「{0}」by {1}は、幸福感に包まれるような懐かしく優しいメロディーに乗せて、静かに眠るイメージを表現しています。\nリズムに合わせてゆったりと指を動かし、放心状態になれる癒やしの一曲です。\nぜひプレイしてリラックスしてください。",
  "一曲オススメするとしたら、「{0}」です。\nこの曲は激しいリズムと美しい旋律が融合されITDTの代表曲です。\n音楽に合わせた動作ができるよう是非挑戦してみてください！",
  "はい、ありますよ！\n「{0}」by {1} は、落ち着きのある雰囲気と美しいメロディが印象的な楽曲です。\n心地よいリズムに乗って、指の動きを緻密にコントロールしてプレイすると、自然と曲に浸ることができます。\n是非、チャレンジしてみてください。",
  "もちろんです！\nおすすめは、「{0}」です。\n{1}の{1}さんの楽曲で、心に響く歌詞とメロディが素敵ですよ。\nBADハマって抜けられません！",
  "{1}の「{0}」っていうんですが、めちゃめちゃ良いんです！\n一度プレイしてみてください、ハマっちゃうかもしれません。",
  "おすすめですか？？「{0}」by {1}はどうでしょう。\nミステリアスで幻想的な雰囲気の一曲です。\nラストも盛り上がりに導かれ、テンションも上がること間違いなしです！\n是非プレイしてみてくださいね。",
  "「{0}」by {1}は、和風の旋律が印象的な楽曲です。\n和太鼓等の和楽器の音色も入っており、日本の文化に触れながらプレイすることができます。\nタップやフリックを駆使して挑戦してみましょう！",
  "もちろん。\n「{0}」は超絶テクニックが必要でとてもむずかしいですが、「{0}」はリズムがつかみやすく、テンポもゆっくりなので初心者の方にもオススメできます。\nそして達成感も存分に味わえると思いますよ。\nぜひ挑戦してみてください！",
  "もちろんです！\n「{0}」はリズミカルかつエモーショナルで、ITDTの世界観を深く感じさせてくれます。\nフレーズが派手なので打ちやすく、スコアアタックにも最適です！",
  "「{0}」by {1}は、壮大で荘厳なメロディーが特徴的な楽曲です。\n想像力が刺激され、プレイする過程で感情が高まっていくのを感じることができます。\nフォーマルな曲調なので、きちんと姿勢を正してプレイするときっと肩甲骨に効きますよ！",
  "あっ、おすすめなら、「{0}」という曲がおススメです！\n{1}の作曲で、独特な曲調に惹かれたんですが、エモーショナルなメロディが胸に響きます。\n私、最近これにハマっちゃって、ぜひおすすめしたいと思って。",
  "「{0}」があります。\nこちらの曲はリズムが複雑で鮮やかなグラフィックとハイスキルの興奮が楽しめます。\n特にオンラインランキング戦で他のプレイヤーと競い合いだしたい方にオススメです！"
]


@bot.slash_command(name="random", description="難易度表から1曲ランダムに表示します。")
async def _slash_random(ctx, level: Option(str,
                                           "難易度を指定します(空欄で全曲)",
                                           required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db))
        fnlevel = song_db[rnd]['level']
  else:
    rnd = random.randrange(len(song_db))
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(name="random_multi", description="難易度表から複数曲ランダムに表示します。")
async def _slash_random_multi(ctx, times: Option(int,
                                                 "抽選曲数を指定します(最大25曲)",
                                                 required=True)):
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  for i in range(times):
    rnd = random.randrange(len(song_db))
    title = song_db[rnd]['title']
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed.add_field(name="[" + str(i + 1) + "]",
                    value="[★" + chlevel + " " + title + "](" + url + ")",
                    inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name="random_range_multi",
                   description="範囲内の難易度から複数曲ランダムに表示します。")
async def _slash_random_range_multi(ctx, times: Option(int,
                                                       "抽選曲数を指定します(最大25曲)",
                                                       required=True),
                                    min: Option(int,
                                                "最低難易度を指定します(空欄で0)",
                                                default=0),
                                    max: Option(int,
                                                "最高難易度を指定します(空欄で25)",
                                                default=25)):
  error = False
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  if min < -1: min = 0
  if max > 104: max = 99
  if min > max:
    print('incorrect')
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    for i in range(times):
      title = ""
      chlevel = ""
      fnlevel = -1
      while not (fnlevel >= min and fnlevel <= max):
        rnd = random.randrange(len(song_db))
        if song_db[rnd]['level'] in ["???"]:
          fnlevel = 101
        elif song_db[rnd]['level'] in ["(^^)"]:
          fnlevel = 102
        elif song_db[rnd]['level'] in ["∞"]:
          fnlevel = 103
        elif song_db[rnd]['level'] in ["NaN"]:
          fnlevel = 104
        else:
          fnlevel = int(song_db[rnd]['level'])
      title = song_db[rnd]['title']
      chlevel = song_db[rnd]['level']
      url = song_db[rnd]['url']
      embed.add_field(name="[" + str(i + 1) + "]",
                    value="[★" + chlevel + " " + title + "](" + url + ")",
                    inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(name="random_illegular",
                   description="難易度表のうち特殊難易度(99,???,(^^),∞,NaN)から1曲ランダムに表示します。"
                   )
async def _slash_random_illegular(ctx, ):
  error = False
  fnlevel = None
  while fnlevel not in ["99", "???", "(^^)", "∞", "NaN"]:
    #print('searching')
    rnd = random.randrange(len(song_db))
    fnlevel = song_db[rnd]['level']
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="特殊難易度ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="random_weighted", description="難易度表から1曲ランダムに表示します。一定の重み付けがなされています。")
async def _slash_random_weighted(ctx):
  error = False
  fnlevel = None
  level = random.choice(["0","0","0","0","0","1","1","1","1","1","2","2","2","2","2","3","3","3","3","3","4","4","4","4","4","5","5","5","5","5","6","6","6","6","6","7","7","7","7","7","8","8","8","8","8","9","9","9","9","9","10","10","10","10","10","11","11","11","12","12","12","13","13","13","14","14","14","15","15","15","16","17","18","19","20","21","22","23","24","25","99","99","99","99","99","∞","∞","∞","∞","∞","???","???","???","???","???","(^^)","(^^)","(^^)","(^^)","(^^)"])
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db))
        fnlevel = song_db[rnd]['level']
  else:
    rnd = random.randrange(len(song_db))
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="random_with_option",
                   description="難易度表から1曲とプレイオプションをランダムに表示します。")
async def _slash_random_with_option(
  ctx, level: Option(str, "難易度を指定します(空欄で全曲)", required=False),
  illegular: Option(int,
                    "数が大きいほどマニアック・高難易度なオプションが出現します。(0~3の範囲で入力 空欄で0)",
                    default=0),
  option_select: Option(
    str,
    "更にランダム要素のあるオプションを直接設定することができます。(空欄でランダム)",
    required=False,
    autocomplete=discord.utils.basic_autocomplete(all_random_options))):
  error = False
  fnlevel = None
  option_list = copy.copy(options[0])
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db))
        fnlevel = song_db[rnd]['level']
  else:
    rnd = random.randrange(len(song_db))
  if not (-1 < illegular < 4):
    embed_err = discord.Embed(title="エラー",
                              description="illegularは0~3の範囲で入力してください。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  else:
    if not option_select:
      print(option_list)
      if illegular >= 1:
        option_list.extend(options[1])
        print(option_list)
        if illegular >= 2:
          option_list.extend(options[2])
          print(option_list)
          if illegular == 3:
            option_list.extend(options[3])
            print(option_list)
      print(option_list)
      rnd_option = random.randrange(len(option_list))
      tmp_option = option_list[rnd_option]
    else:
      if option_select not in all_random_options:
        embed_err = discord.Embed(
          title="エラー",
          description="指定されたオプションは存在しないか、ランダム要素がありません。",
          color=0xff8080)
        await ctx.respond(embed=embed_err, ephemeral=True)
        error = True
      else:
        tmp_option = option_select
    if tmp_option == "Reg.Speed":
      tmp_option += (" " + str(20 + (20 * random.randrange(1, 14))))
    if tmp_option == "PlaySpeed(Easy)":
      tmp_option += (":" + str(round(random.uniform(0.25, 1), 2)))
    if tmp_option == "PlaySpeed":
      tmp_option += (":" + str(round(random.uniform(1, 1.5), 2)))
    if tmp_option == "PlaySpeed(Hard)":
      tmp_option += (":" + str(round(random.uniform(1.5, 4.0), 1)))
    if tmp_option == "JudgeRange":
      tmp_option += (":[" + str(50 + (5 * (random.randrange(1, 4)))) + "," +
                     str(100 + (10 * (random.randrange(1, 4)))) + "," +
                     str(200 + (20 * (random.randrange(1, 4)))) + "]")
    if tmp_option == "JudgeRange(Hard)":
      tmp_option += (":[" + str(20 + (5 * (random.randrange(1, 6)))) + "," +
                     str(40 + (10 * (random.randrange(1, 6)))) + "," +
                     str(80 + (20 * (random.randrange(1, 6)))) + "]")
    if tmp_option == "JudgeRange(S-Random)":
      tmp_option += (":[" + str(random.randrange(1, 250)) + "," +
                     str(random.randrange(1, 500)) + "," +
                     str(random.randrange(1, 1000)) + "]")
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(オプション付き)", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    embed.add_field(name="オプション", value=tmp_option, inline=False)
    await ctx.respond(embed=embed)


@bot.command(
  name="random_range",
  description="範囲内の難易度から1曲ランダムに表示します。???,(^^),∞,NaNは対象外です。",
)
async def _slash_random_range(ctx, min: Option(int,
                                               "最低難易度を指定します(空欄で0)",
                                               default=0),
                              max: Option(int,
                                          "最高難易度を指定します(空欄で25)",
                                          default=25)):
  error = False
  fnlevel = -1
  if min < -1: min = 0
  if max > 100: max = 99
  if min > max:
    print('incorrect')
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  else:
    while not (fnlevel >= min and fnlevel <= max):
      rnd = random.randrange(len(song_db))
      if song_db[rnd]['level'] in ["???", "(^^)", "∞", "NaN"]:
        fnlevel = 101
      else:
        fnlevel = int(song_db[rnd]['level'])

  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="範囲ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.command(name="random_nd", description="指定されたND名を含むの譜面から1曲ランダムに表示します。")
async def _slash_random_nd(ctx, nd: Option(str, "ND名を指定します", required=True)):
  error = False
  nd = "obj:" + nd
  fnd = ""
  count = 0
  while not (nd in fnd):
    rnd = random.randrange(len(song_db))
    fnd = song_db[rnd]['subtitle']
    count += 1
    if count > len(song_db):
      embed_err = discord.Embed(title="エラー",
                                description="指定されたNDの譜面が見つかりませんでした。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
      break
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    embed = discord.Embed(title="ND指定ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.command(
  name="random_dan",
  description="指定された段位相当のコースをランダムに生成します。",
)
async def _slash_random_dan(ctx, dan: Option(
  str,
  "段位を指定します。(ビギナー,初段～十段,皆伝,Overjoy)",
  required=True,
  autocomplete=discord.utils.basic_autocomplete([
    "ビギナー", "初段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "十段", "皆伝",
    "Overjoy"
  ]),
), duplication: Option(bool, "曲被りの有無を指定します。(空欄でTrue(被りあり))", default=True)):
  error = False
  titles = ["", "", "", ""]
  chlevels = [-1, -1, -1, -1]
  urls = ["", "", "", ""]
  chartnum = [0, 0, 0, 0]
  fnlevel = None
  if dan not in [
      "ビギナー", "初段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "十段", "皆伝",
      "Overjoy", "Undefined", "Unplayable", "Thinking", "Test"
  ]:
    print('not defined')
    embed_err = discord.Embed(title="エラー",
                              description="指定された段位は存在しません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    for i in range(4):
      fnlevel = None
      while fnlevel != dan_level[dan][i]:
        rnd = random.randrange(len(song_db))
        if song_db[rnd]['level'] in ["???", "(^^)", "∞", "NaN"]:
          fnlevel = 101
        elif duplication == False and rnd in chartnum:
          fnlevel = 777
        else:
          fnlevel = int(song_db[rnd]['level'])
      titles[i] = song_db[rnd]['title'].replace('_', '\_')
      chlevels[i] = song_db[rnd]['level']
      urls[i] = song_db[rnd]['url']
      chartnum[i] = rnd

    embed = discord.Embed(title="ランダム段位", color=0xff8080)
    embed.add_field(name="1曲目",
                    value="★" + chlevels[0] + " " + titles[0],
                    inline=False)
    embed.add_field(name="URL", value=urls[0], inline=True)
    embed.add_field(name="2曲目",
                    value="★" + chlevels[1] + " " + titles[1],
                    inline=False)
    embed.add_field(name="URL", value=urls[1], inline=True)
    embed.add_field(name="3曲目",
                    value="★" + chlevels[2] + " " + titles[2],
                    inline=False)
    embed.add_field(name="URL", value=urls[2], inline=True)
    embed.add_field(name="4曲目",
                    value="★" + chlevels[3] + " " + titles[3],
                    inline=False)
    embed.add_field(name="URL", value=urls[3], inline=True)
    await ctx.respond(embed=embed)

#ここから下は特殊難易度表ランダム

@bot.slash_command(name="sl_random", description="低速難易度表から1曲ランダムに表示します。")
async def _slash_sl_random(ctx, level: Option(str,
                                              "難易度を指定します(空欄で全曲)",
                                              required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_sl))
        fnlevel = song_db_sl[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_sl))
  if error != True:
    title = song_db_sl[rnd]['title'].replace('_', '\_')
    chlevel = song_db_sl[rnd]['level']
    url = song_db_sl[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(低速難易度表)", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="$" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(name="lg_random", description="長尺・短尺まとめ表から1曲ランダムに表示します。")
async def _slash_lg_random(ctx, level: Option(str,
                                              "難易度を指定します(空欄で全曲)",
                                              required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in [
        "__", "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "6",
        "7", "8", "9", "10"
    ]:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_lg))
        fnlevel = song_db_lg[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_lg))
  if error != True:
    title = song_db_lg[rnd]['title'].replace('_', '\_')
    chlevel = song_db_lg[rnd]['level']
    time = song_db_lg[rnd]['time']
    url = song_db_lg[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(長尺・短尺まとめ表)", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="長" + chlevel, inline=False)
    embed.add_field(name="演奏時間", value=time, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(name="st_random", description="長複合難易度表から1曲ランダムに表示します。")
async def _slash_st_random(ctx, level: Option(str,
                                              "難易度を指定します(空欄で全曲)",
                                              required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13",
        "14", "15", "16", "17", "18", "19", "20"
    ]:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_st))
        fnlevel = song_db_st[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_st))
  if error != True:
    title = song_db_st[rnd]['title'].replace('_', '\_')
    chlevel = song_db_st[rnd]['level']
    url = song_db_st[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(長複合難易度表)", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="◆" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="ds_random", description="Lodestar難易度表から1曲ランダムに表示します。")
async def _slash_ds_random(ctx, level: Option(str,
                                              "難易度を指定します(空欄で全曲)",
                                              required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in ["0","1", "2", "3", "4", "5", "6", "7", "8", "9", "10","11","12"]:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_ds))
        fnlevel = song_db_ds[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_ds))
  if error != True:
    title = song_db_ds[rnd]['title'].replace('_', '\_')
    chlevel = song_db_ds[rnd]['level']
    url = song_db_ds[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(Lodestar難易度表)", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="ds" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="dp_random", description="DP難易度表から1曲ランダムに表示します。")
async def _slash_dp_random(ctx, level: Option(str,
                                              "難易度を指定します(空欄で全曲)",
                                              required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in all_levels_dp:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_dp))
        fnlevel = song_db_dp[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_dp))
  if error != True:
    title = song_db_dp[rnd]['title'].replace('_', '\_')
    chlevel = song_db_dp[rnd]['level']
    url = song_db_dp[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="Φ" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.command(
  name="dp_random_range",
  description="範囲内の難易度から1曲ランダムに表示します。???,Φは対象外です。",
)
async def _slash_dp_random_range(ctx, min: Option(int,
                                              "最低難易度を指定します(空欄で0)",
                                              default=0),
                                max: Option(int,
                                              "最高難易度を指定します(空欄で15)",
                                              default=15)):
  error = False
  fnlevel = -1
  if min < -1: min = 0
  if max > 100: max = 99
  if min > max:
    print('incorrect')
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  else:
    while not (fnlevel >= min and fnlevel <= max):
      rnd = random.randrange(len(song_db_dp))
      if song_db_dp[rnd]['level'] in ["???", "Φ"]:
        fnlevel = 101
      else:
        fnlevel = int(song_db_dp[rnd]['level'])

  if error != True:
    title = song_db_dp[rnd]['title'].replace('_', '\_')
    chlevel = song_db_dp[rnd]['level']
    url = song_db_dp[rnd]['url']
    embed = discord.Embed(title="範囲ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="Φ" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="dp_random_multi", description="DP難易度表から複数曲ランダムに表示します。")
async def _slash_dp_random_multi(ctx, times: Option(int,
                                                 "抽選曲数を指定します(最大25曲)",
                                                 required=True)):
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  for i in range(times):
    rnd = random.randrange(len(song_db_dp))
    title = song_db_dp[rnd]['title'].replace('_', '\_')
    chlevel = song_db_dp[rnd]['level']
    embed.add_field(name="[" + str(i + 1) + "]",
                    value="Φ" + chlevel + " " + title,
                    inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name="dp_random_range_multi",
                   description="範囲内の難易度からDP譜面を複数曲ランダムに表示します。")
async def _slash_dp_random_range_multi(ctx, times: Option(int,
                                                       "抽選曲数を指定します(最大25曲)",
                                                       required=True),
                                    min: Option(int,
                                                "最低難易度を指定します(空欄で0)",
                                                default=0),
                                    max: Option(int,
                                                "最高難易度を指定します(空欄で15)",
                                                default=15)):
  error = False
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  if min < -1: min = 0
  if max > 102: max = 99
  if min > max:
    print('incorrect')
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    for i in range(times):
      title = ""
      chlevel = ""
      fnlevel = -1
      while not (fnlevel >= min and fnlevel <= max):
        rnd = random.randrange(len(song_db_dp))
        if song_db_dp[rnd]['level'] in ["???"]:
          fnlevel = 101
        elif song_db_dp[rnd]['level'] in ["Φ"]:
          fnlevel = 102
        else:
          fnlevel = int(song_db_dp[rnd]['level'])
      title = song_db_dp[rnd]['title'].replace('_', '\_')
      chlevel = song_db_dp[rnd]['level']
      embed.add_field(name="[" + str(i + 1) + "]",
                      value="Φ" + chlevel + " " + title,
                      inline=False)
    await ctx.respond(embed=embed)
    
#大会用
@bot.slash_command(name="random_tournament",
                   description="大会IDを指定して1曲ランダムに表示します。")
async def _slash_random_tournament(ctx, id: Option(
  str,
  "大会IDを指定します",
  required=True,
  autocomplete=discord.utils.basic_autocomplete(all_tournament))):
  error = False
  fntournament = None
  if id not in all_tournament:
    print('not defined')
    embed_err = discord.Embed(title="エラー",
                              description="指定された大会は存在しません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  else:
    while fntournament != id:
      print('searching')
      rnd = random.randrange(len(song_db_tm))
      fntournament = song_db_tm[rnd]['tnmid']
  if error != True:
    title = song_db_tm[rnd]['title'].replace('_', '\_')
    chlevel = song_db_tm[rnd]['level']
    url = song_db_tm[rnd]['url']
    embed = discord.Embed(title="ランダム選曲(" + id + ")", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)


@bot.slash_command(name="search_title", description="タイトル・差分名で検索します。(2文字以上)")
async def _slash_search_title(ctx, word: Option(str,
                                                "検索語句を入力します",
                                                required=False),
                              ephemeral: Option(
                                bool,
                                "Trueにすると自分にしか表示されなくなります。(デフォルトはFalse)",
                                required=False,
                                default=False)):
  error = False
  if len(word) < 2:
    embed_err = discord.Embed(title="エラー",
                              description="検索語句は2文字以上にしてください。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    found_num = []
    for i in range(len(song_db)):
      if word in song_db[i]['title']:
        found_num.append(i)
    embed = discord.Embed(title="検索結果", color=0xff8080)
    count = 1
    if not found_num:
      embed.add_field(name="[0]",
                      value="指定された語句を含む譜面が見つかりませんでした。",
                      inline=False)
    for i in found_num:
      title = song_db[i]['title']
      chlevel = song_db[i]['level']
      url = song_db[i]['url'] 
      embed.add_field(name="[" + str(count) + "]",
                    value="[★" + chlevel + " " + title + "](" + url + ")",
                    inline=False) 
      count += 1
      if (count >= 25): break
    await ctx.respond(embed=embed, ephemeral=ephemeral)

@bot.slash_command(name="dp_search_title", description="DP譜面をタイトル・差分名で検索します。(2文字以上)")
async def _slash_dp_search_title(ctx, word: Option(str,
                                                "検索語句を入力します",
                                                required=False),
                              ephemeral: Option(
                                bool,
                                "Trueにすると自分にしか表示されなくなります。(デフォルトはFalse)",
                                required=False,
                                default=False)):
  error = False
  if len(word) < 2:
    embed_err = discord.Embed(title="エラー",
                              description="検索語句は2文字以上にしてください。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    found_num = []
    for i in range(len(song_db_dp)):
      if word in song_db_dp[i]['title']:
        found_num.append(i)
    embed = discord.Embed(title="検索結果", color=0xff8080)
    count = 1
    if not found_num:
      embed.add_field(name="[0]",
                      value="指定された語句を含む譜面が見つかりませんでした。",
                      inline=False)
    for i in found_num:
      title = song_db_dp[i]['title']
      chlevel = song_db_dp[i]['level']
      url = song_db_dp[i]['url']
      embed.add_field(name="[" + str(count) + "]",
                    value="[Φ" + chlevel + " " + title + "](" + url + ")",
                    inline=False) 
      count += 1
      if (count >= 25): break
    await ctx.respond(embed=embed, ephemeral=ephemeral)

@bot.slash_command(name="score")
async def _slash_score(ctx, great: Option(int, "良の数", required=True),
                       good: Option(int, "可の数",
                                    required=True), bad: Option(int,
                                                                "不可の数",
                                                                required=True),
                       type: Option(int,
                                    "スコアのタイプ(0でEXSCORE,1でGAUGESCORE(デフォルト))",
                                    required=False,
                                    default=1), ephemeral: Option(
                                      bool,
                                      "Trueにすると自分にしか表示されなくなります。(デフォルトはTrue)",
                                      required=False,
                                      default=True)):
  if type == 0:
    await ctx.respond(
      f"EXSCORE:{great*2 + good}/{(great + good + bad)*2}(MAX-{((great + good + bad)*2)-(great*2 + good)})",
      ephemeral=ephemeral)
  elif type == 1:
    await ctx.respond(
      f"GAUGESCORE:{great*2 + good - bad*4}/{(great + good + bad)*2}(MAX-{((great + good + bad)*2)-(great*2 + good - bad*4)})",
      ephemeral=ephemeral)
  else:
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)

@bot.slash_command(name="frequency")
async def _slash_frequency(ctx, freq: Option(float, "楽曲キー変更量", required=True)): # type: ignore
    ps = str(round(2**(freq/12),6))
    ps_str = ps + "0"*(8-len(ps))  
    ps_txt = "Playspeed=" + ps_str
    ps = float(ps)
    j1_txt = "JudgeRangeGreat=" + str(int(60*ps))
    j2_txt = "JudgeRangeGood=" + str(int(120*ps))
    j3_txt = "JudgeRangeBad=" + str(int(240*ps))
    if (ps > 4) or (ps < 0.25):
      embed_err = discord.Embed(title="エラー",
                              description="Playspeedが次郎の対応範囲を超えました。",
                              color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
    else:
      await ctx.respond(f"{ps_txt}\n{j1_txt}\n{j2_txt}\n{j3_txt}")

@bot.slash_command(name="kill")
async def _slash_kill(ctx):
  await ctx.respond(f"{ctx.user.name}は奈落の底へ落ちた")


@bot.slash_command(name="gamerule")
async def _slash_gamerule(
    ctx,
    gamerule: Option(str, required=True),
    value: Option(str, required=True),
):
  await ctx.respond(f"ゲームルール {gamerule} が {value} に設定されました")

@bot.slash_command(name="join")
async def _slash_join(ctx):
      if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()

@bot.slash_command(name="leave")
async def _slash_leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.slash_command(name="leveljudge")
async def _slash_leveljudge(ctx, chart: Option(str, required=True)):
  level = all_levels[random.randrange(len(all_levels))]
  await ctx.respond(f"{chart}は★{level}です。")

@bot.slash_command(name="dp_leveljudge")
async def _slash_dp_leveljudge(ctx, chart: Option(str, required=True)):
  level = all_levels_dp[random.randrange(len(all_levels_dp))]
  await ctx.respond(f"{chart}はΦ{level}です。")

@bot.slash_command(name="bpmjudge")
async def _slash_bpmjudge(ctx, chart: Option(str, required=True)):
  level = random.randrange(1, 999)
  await ctx.respond(f"{chart}は{level}BPMです。")

@bot.slash_command(name="factcheck")
async def _slash_factcheck(ctx, chart: Option(str, required=True)):
  truefalse = random.randint(1,2)
  if truefalse == 1:
    await ctx.respond(f"{chart}は真です。")
  else:
    await ctx.respond(f"{chart}は偽です。")

@bot.slash_command(name="brv1_random", description="？？？？から1曲ランダムに表示します。 利用にはキーコードが必要です")
async def _slash_brv1_random(ctx, keycode: Option(str,
                                           "KeyCode11",
                                           required=True),
                                  level: Option(str,
                                        "難易度を指定します(空欄で全曲)",
                                        required=False)):
  error = False
  fnlevel = None
  if keycode != "Sea5671":
      embed_err = discord.Embed(title="エラー",
                                description="キーコードが正しくありません",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
  else:
    if level:
      print('not empty')
      if level not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13","???"]:
        print('not defined')
        embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
        await ctx.respond(embed=embed_err, ephemeral=True)
        error = True
      else:
        while fnlevel != level:
          #print('searching')
          rnd = random.randrange(len(song_db_pk))
          fnlevel = song_db_pk[rnd]['level']
    else:
      rnd = random.randrange(len(song_db_pk))
  if error != True:
    title = song_db_pk[rnd]['title'].replace('_', '\_')
    chlevel = song_db_pk[rnd]['level']
    url = song_db_pk[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)
    

@bot.slash_command(name="hard_random", description="難しい楽曲を1曲ランダムに表示します。")
async def _slash_hard_random(ctx, ):
  rnd = random.randrange(len(song_db_hd))
  title = song_db_hd[rnd]['title'].replace('_', '\_')
  chlevel = song_db_hd[rnd]['level']
  url = song_db_hd[rnd]['url']
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  embed.add_field(name="曲名", value=title, inline=False)
  embed.add_field(name="難易度", value="★" + chlevel, inline=False)
  embed.add_field(name="URL", value=url, inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name="easy_random", description="易しい楽曲を1曲ランダムに表示します。")
async def _slash_easy_random(ctx, ):
  rnd = random.randrange(len(song_db_ez))
  title = song_db_ez[rnd]['title'].replace('_', '\_')
  chlevel = song_db_ez[rnd]['level']
  url = song_db_ez[rnd]['url']
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  embed.add_field(name="曲名", value=title, inline=False)
  embed.add_field(name="難易度", value="★" + chlevel, inline=False)
  embed.add_field(name="URL", value=url, inline=False)
  await ctx.respond(embed=embed)


@bot.slash_command(name="sega_random", description="チュウニズムの譜面を1曲ランダムに表示します。")
async def _slash_sega_random(ctx, ):
  rnd = random.randrange(len(song_db_sg))
  title = song_db_sg[rnd]['title'].replace('_', '\_')
  chlevel = song_db_sg[rnd]['level']
  url = song_db_sg[rnd]['url']
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  embed.add_field(name="曲名", value=title, inline=False)
  embed.add_field(name="難易度", value="★" + chlevel, inline=False)
  embed.add_field(name="URL", value=url, inline=False)
  await ctx.respond(embed=embed)

@bot.slash_command(name="nds_random", description="ニンテンドーDSで発売されたゲームソフトから1本ランダムに表示します。")
async def _slash_nds_random(ctx):
  rnd = random.randrange(len(song_db_nds))
  title = song_db_nds[rnd]['title'].replace('_', '\_')
  date = song_db_nds[rnd]['date']
  maker = song_db_nds[rnd]['maker']
  embed = discord.Embed(title="ランダム選出", color=0xff8080)
  embed.add_field(name="タイトル", value=title, inline=False)
  embed.add_field(name="発売日", value=date, inline=False)
  embed.add_field(name="メーカー", value=maker, inline=False)
  await ctx.respond(embed=embed)

@bot.slash_command(name="psp_random", description="PowerSuperPower難易度表から1曲ランダムに表示します。")
async def _slash_psp_random(ctx, level: Option(str,
                                           "難易度を指定します(空欄で全曲)",
                                           required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db_psp))
        fnlevel = song_db_psp[rnd]['level']
  else:
    rnd = random.randrange(len(song_db_psp))
  if error != True:
    title = song_db_psp[rnd]['title'].replace('_', '\_')
    chlevel = song_db_psp[rnd]['level']
    url = song_db_psp[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="psp" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.command(
  name="random_keyconf",
  description="keyconf.iniをランダムに生成します。",
)
async def _slash_random_keyconf(ctx):
  rnd_1 = random.randrange(48, 91)
  rnd_2 = random.randrange(48, 91)
  rnd_3 = random.randrange(48, 91)
  rnd_4 = random.randrange(48, 91)

  templete = "```\n[KeyAssignment]\nL_KaP1={0}\nL_DongP1={1}\nR_DongP1={2}\nR_KaP1={3}\n```"
  text = templete.format(rnd_1, rnd_2, rnd_3, rnd_4)
  await ctx.respond(text)


@bot.slash_command(name="random_number", description="指定された範囲内の乱数を表示します。")
async def _slash_random_number(ctx, min: Option(int, required=True),
                             max: Option(int, required=True)):
  rnd = random.randint(min, max)
  await ctx.respond(rnd)

@bot.slash_command(name="random_number_multi", description="指定された範囲内の乱数を複数表示します。")
async def _slash_random_number_multi(ctx, min:   Option(int,  required=True),
                                          max:   Option(int,  required=True),
                                          times: Option(int,  required=True),
                                          sort:  Option(bool, default=False)):
  rnd = []
  for i in range(times):
    rnd.append(random.randint(min, max))
  if (sort == True):
    rnd.sort()
  await ctx.respond(rnd)

# @bot.slash_command(name="bingo", description="ビンゴの条件を表示します。")
# async def _slash_bingo(ctx):

#   terms = ""
#   rnd = random.randrange(1, 100)
#   if rnd <= 1:
#     #1%
#     terms = "FullCombo(フルコンボをすることで開けることができます)"
#   elif rnd <= 5:
#     #4%
#     terms = "HardClear(ハードクリアをすることで開けることができます)"
#   elif rnd <= 30:
#     #25%
#     terms = "Clear(クリアをすることで開けることができます)"
#   else:
#     #70%
#     terms = "Hit(無条件で開けることができます)"

#   embed = discord.Embed(title="ITDTビンゴ", color=0xff8080)
#   embed.add_field(name="条件", value=terms, inline=False)
#   await ctx.respond(embed=embed)


@bot.slash_command(name="mememe_dice", description="「めめめのサイコロが！」を表示します。")
async def _slash_mememe_dice(ctx):
  rnd = random.randint(1, 2)
  if rnd == 1:
    await ctx.respond("https://www.nicovideo.jp/watch/sm34094775")
  elif rnd == 2:
    await ctx.respond("https://soundcloud.com/araittt/off24bit")


@bot.slash_command(name="random_dice", description="「ランダムダイス」を表示します。")
async def _slash_random_dice(ctx):
  await ctx.respond("https://twitter.com/RandomDice_JP")


@bot.slash_command(name="rice", description="「ライス」を表示します。")
async def _slash_rice(ctx):
  await ctx.respond(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Meshi_002.jpg/1280px-Meshi_002.jpg"
  )


@bot.slash_command(name="mememe_rice", description="「mememe_rice」を表示します。")
async def _slash_mememe_rice(ctx):
  await ctx.respond("https://www.youtube.com/watch?v=YUJLEN0_v5A")


@bot.slash_command(name="stream_gen", description="stream_genします。")
async def _slash_stream_gen(ctx, length: Option(int, required=True)):
  result = ""
  lastnote = 0
  for i in range(length):
    counter = 0
    if lastnote == 1:
      result += "2"
    else:
      result += "1"
    while counter < 16:
      notes = random.randrange(1, 3)
      color = random.randrange(1, 2)
      for d in range(notes):
        if counter == 16:
          lastnote = int(result[-1])
          break
        else:
          if color == 1:
            result += "1"
          else:
            result += "2"
          counter += 1
    result += ",\n"
  await ctx.respond(result)


@bot.slash_command(name="parallax_gen", description="parallax_genします。")
async def _slash_parallax_gen(ctx):
  result = "1222122212221222,\n1222122212221222,\n1122112211221122,\n1122112211221122,\n1112111211121112,\n1112111211121112,\n1121112111211121,\n1121112111211121,\n"
  await ctx.respond(result)


@bot.slash_command(name="random_minun",
                   description="ポケモン図鑑から複数マイナンをランダムに表示します。")
async def _slash_random_minun(ctx, times: Option(int, required=False)):
  result = ""
  for i in range(random.randrange(50)):
    if random.randrange(2) == 0:
      result += "<:minun:1109034104705523752>"
    else:
      result += "<a:minun_moving:1036647842229522454>"
  if result == "":
    result += "<:purin:1109034149471330304>"
  await ctx.respond(result)


@bot.slash_command(name="random_diffname", description="差分名をランダムに表示します。")
async def _slash_random_diffname(ctx):
  response = requests.get('https://random-word-api.herokuapp.com/word')
  await ctx.respond("[" + response.json()[0] + "]")

@bot.slash_command(name="random_groupname", description="ITDT Random")
async def _slash_random_groupname(ctx):
  word_i  = requests.get('https://random-word-api.vercel.app/api?words=1&letter=i&type=capitalized')
  word_t1 = requests.get('https://random-word-api.vercel.app/api?words=1&letter=t&type=capitalized')
  word_d  = requests.get('https://random-word-api.vercel.app/api?words=1&letter=d&type=capitalized')
  word_t2 = requests.get('https://random-word-api.vercel.app/api?words=1&letter=t&type=capitalized')
  result_eng = word_i.json()[0] + " " + word_t1.json()[0] + " " + word_d.json()[0] + " " + word_t2.json()[0] + " "
  await ctx.respond(result_eng)

@bot.slash_command(name="random_groupname_f4p", description="F4P Random")
async def _slash_random_groupname(ctx):
  word_f  = requests.get('https://random-word-api.vercel.app/api?words=1&letter=f&type=capitalized')
  word_p  = requests.get('https://random-word-api.vercel.app/api?words=1&letter=p&type=capitalized')
  result_eng = word_f.json()[0] + " 4 " + word_p.json()[0]
  await ctx.respond(result_eng)

@bot.slash_command(name="random_kanji",
                   description="漢字(漢検一級範囲内)をランダムに1~4文字表示します。")
async def _slash_random_kanji(ctx):
  result = ""
  for i in range(random.randint(1, 4)):
    rnd = random.randrange(len(kanji_db))
    result += kanji_db[rnd]
  await ctx.respond(result)


@bot.slash_command(name="ai_chan", description="バーチャルAIアシスタント")
async def _slash_ai_chan(ctx, level: Option(str,
                                            "難易度を指定します(空欄で全曲)",
                                            required=False)):
  global count
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      while fnlevel != level:
        #print('searching')
        rnd = random.randrange(len(song_db))
        fnlevel = song_db[rnd]['level']
  else:
    rnd = random.randrange(len(song_db))
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    subtitle = song_db[rnd]['subtitle'].replace('_', '\_')
    chlevel = song_db[rnd]['level']
    url = song_db[rnd]['url']
    ai_responce = ai_chan[random.randrange(len(ai_chan))].format(
      title, subtitle)
    embed = discord.Embed(title="AI-Chan", color=0xff8080)
    embed.add_field(name="返答", value=ai_responce, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="super_random", description="難易度表から1曲ランダムに表示します。レベルもランダムに決定されます。")
async def _slash_super_random(ctx, level: Option(str,
                                           "難易度を指定します(空欄で全曲)",
                                           required=False)):
  error = False
  fnlevel = None
  if level:
    print('not empty')
    if level not in all_levels:
      print('not defined')
      embed_err = discord.Embed(title="エラー",
                                description="指定された難易度は存在しません。",
                                color=0xff8080)
      await ctx.respond(embed=embed_err, ephemeral=True)
      error = True
    else:
      rnd = random.randrange(len(song_db))
      fnlevel = level
  else:
    rnd = random.randrange(len(song_db))
    fnlevel = random.choice(all_levels)
  if error != True:
    title = song_db[rnd]['title'].replace('_', '\_')
    chlevel = fnlevel
    url = song_db[rnd]['url']
    embed = discord.Embed(title="ランダム選曲", color=0xff8080)
    embed.add_field(name="曲名", value=title, inline=False)
    embed.add_field(name="難易度", value="★" + chlevel, inline=False)
    embed.add_field(name="URL", value=url, inline=False)
    await ctx.respond(embed=embed)

@bot.slash_command(name="super_random_range_multi",
                   description="範囲内の難易度から複数曲ランダムに表示します。レベルもランダムに決定されます。")
async def _slash_super_random_range_multi(ctx, times: Option(int,
                                                       "抽選曲数を指定します(最大25曲)",
                                                       required=True),
                                    min: Option(int,
                                                "最低難易度を指定します(空欄で0)",
                                                default=0),
                                    max: Option(int,
                                                "最高難易度を指定します(空欄で25)",
                                                default=25)):
  error = False
  embed = discord.Embed(title="ランダム選曲", color=0xff8080)
  if min < -1: min = 0
  if max > 104: max = 99
  if min > max:
    print('incorrect')
    embed_err = discord.Embed(title="エラー",
                              description="入力形式が正しくありません。",
                              color=0xff8080)
    await ctx.respond(embed=embed_err, ephemeral=True)
    error = True
  if error != True:
    for i in range(times):
      title = ""
      chlevel = ""
      fnlevel = -1
      fnlevelstr = ""
      while not (fnlevel >= min and fnlevel <= max):
        rnd = random.randrange(len(song_db))
        fnlevelstr = random.choice(all_levels)
        if fnlevelstr == "???":
          fnlevel = 101
        elif fnlevelstr == "(^^)":
          fnlevel = 102
        elif fnlevelstr == "∞":
          fnlevel = 103
        elif fnlevelstr == "NaN":
          fnlevel = 104
        else:
          fnlevel = int(fnlevelstr)
      title = song_db[rnd]['title'].replace('_', '\_')
      chlevel = fnlevelstr
      embed.add_field(name="[" + str(i + 1) + "]",
                      value="★" + chlevel + " " + title,
                      inline=False)
    await ctx.respond(embed=embed)

@bot.event
async def on_ready():
  print('log in')
  loop.start()
  #activity = discord.Activity(name='14 Minesweeper Variants',
  #                            type=discord.ActivityType.playing)
  activity = discord.Activity(name='ITDTの譜面',
                              type=discord.ActivityType.playing)
  await bot.change_presence(activity=activity)


@tasks.loop(seconds=60)
async def loop():
  now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%H:%M')
  #print(f"loop:{now}")
  if now == '00:00':
    global song_db
    global song_db_sl
    global song_db_lg
    global song_db_st
    global song_db_dp
    global song_db_pk
    
    res = requests.get(db_url)
    res_sl = requests.get(db_url_sl)
    res_lg = requests.get(db_url_lg)
    res_st = requests.get(db_url_st)
    res_dp = requests.get(db_url_dp)
    res_pk = requests.get(db_url_pk)

    song_db = json.loads(res.text)
    song_db_sl = json.loads(res_sl.text)
    song_db_lg = json.loads(res_lg.text)
    song_db_st = json.loads(res_st.text)
    song_db_dp = json.loads(res_dp.text)
    song_db_pk = json.loads(res_pk.text)

    print('songdb reloaded')
    
    db_shuffle = random.randrange((len(song_db) + len(song_db_dp)))
    channel = bot.get_channel(987348863641878528)

    if (db_shuffle < len(song_db)):
       rnd = db_shuffle
       title = song_db[rnd]['title']
       chlevel = song_db[rnd]['level']
       url = song_db[rnd]['url']
       embed = discord.Embed(title="今日の譜面", color=0xff8080)
       embed.add_field(name="曲名", value=title, inline=False)
       embed.add_field(name="難易度", value="★" + chlevel, inline=False)
       embed.add_field(name="URL", value=url, inline=False)
    else:
       rnd = db_shuffle - len(song_db)
       title = song_db_dp[rnd]['title']
       chlevel = song_db_dp[rnd]['level']
       url = song_db_dp[rnd]['url']
       embed = discord.Embed(title="今日の譜面", color=0xff8080)
       embed.add_field(name="曲名", value=title, inline=False)
       embed.add_field(name="難易度", value="Φ" + chlevel, inline=False)
       embed.add_field(name="URL", value=url, inline=False)

    await channel.send(embed=embed)
  if random.randint(1,2) == 2:
        guild = bot.get_guild(815560489312190504)
        channel = bot.get_channel(1072859349946482768)
        if not guild:
            print("ギルドが見つかりません")
            return

        # 一番人数が多いVCを探す
        target_channel = None
        max_members = 0
        for channel in guild.voice_channels:
            if len(channel.members) > max_members:
                max_members = len(channel.members)
                target_channel = channel

        if target_channel and max_members > 0:
            if not guild.voice_client:
                voice_client = await target_channel.connect()
                print(f"{target_channel} に参加しました！（人数: {max_members}）")

                # 音声再生
                try:
                    source = discord.FFmpegPCMAudio("parallax.mp3")
                    source = discord.PCMVolumeTransformer(source, volume=0.5)
                    voice_client.play(source)

                    # 再生終了まで待つ
                    while voice_client.is_playing():
                        await discord.utils.sleep_until(datetime.now() + timedelta(seconds=1))

                except Exception as e:
                    print(f"音声再生エラー: {e}")
                await voice_client.disconnect()
        else:
            print("15:00時点でどのVCにも誰もいませんでした。")

async def ad_send(ctx):
  embed = discord.Embed(title="【広告】", color=0xff8080)
  embed.add_field(name="放置少女",
                  value="500名以上の美少女たちを集め、キミの戦略で勝利を掴め！",
                  inline=False)
  embed.add_field(name="おねがい社長！",
                  value="美人でスタイル抜群なセクシー秘書が続々登場するハーレム系経営シミュレーションゲーム！！",
                  inline=False)
  embed.add_field(name="発狂次郎難易度表",
                  value="エクストリームな太鼓譜面で次郎界の頂点になる！",
                  inline=False)
  await ctx.respond(embed=embed)

server = HealthCheckServer()
server.start()

bot.run(TOKEN)