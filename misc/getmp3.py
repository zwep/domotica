import requests
import time
import os


download_mp3_list = ['https://content.production.cdn.art19.com/validation=1588072105,8201c93c-88e4-55df-8fd6-3f5ce59480e7,Z5N0aV3uSS_Wy9uxZsuNtrBXQQU/episodes/0395fba1-dbfb-4800-8849-d1026dd4fd09/42ebcda0144e9f3c576a864539caf67ae6419883c76520ef9bb413e1c51f03725940a2fa16c7368f813093ab0161328171c1c0b6a7c803dedecccb54ac16dfda/%2383%3A%20Op%20neutrinojacht%20in%20de%20Middellandse%20zee.mp3',
'https://content.production.cdn.art19.com/validation=1588072129,761a66a5-4349-5e36-a924-2700b575cc4f,H2kA2MWrNuxVw_MsrisWGG8tN_0/episodes/d4a992ed-6c6b-402a-b5d0-a2f99de75ae7/24d802ffa0cdde2d3d6351520600847ebf8126e420c4ff8405e133dd9e6d0debae83d807e13dd3c8960031767104e33e808c5645deae1243ff2070d4f3e41efe/%2370%3A%20Waarom%20zoeken%20we%20naar%20planeten%20buiten%20ons%20zonnestelsel%3F.mp3',
'https://content.production.cdn.art19.com/validation=1588072148,a4e0e6df-9594-5461-b87b-23dc5b9cf443,6O2BDWzE9XPWeevg-S9bSXL7Va0/episodes/e503c8d5-e91d-4c53-a6ba-3e9395925805/8c270deb4c2db366b1b4ba0cf233b0ebd70281762ae94123d298fa1ecf253b37a3ad06842bb9c801484c082acd2bd1f2e3d232c7393e6492075264eac138bb33/%2368%3A%20Kun%20je%20met%20je%20gedachten%20een%20computer%20bedienen%3F.mp3',
'https://content.production.cdn.art19.com/validation=1588072174,23daa89b-e838-5bb1-8382-192310b3106a,xH1MrSqmhRF_t79UGP7e0My6dg4/episodes/7b5e5cd2-7081-4640-9374-0b387693b840/05b910de64d1a1a8442f2b42de348d64c1876d0c9026a362175109be69663a98fd5bf1d362c4e7d6dc59b9e484d12a6ab1e0126b40d819e961cd597fc9d5fa7c/%2363.1%3A%20Nobelprijs%20voor%20cellen%20in%20ademnood.mp3',
'https://content.production.cdn.art19.com/validation=1588072212,10ae9c59-b55b-56a1-9786-2cdb223c91fb,2pz159BR2HdM25Ci4GlkZfcSGFk/episodes/56f1ace4-4046-4f85-be28-d56ae0d15ee4/4838b35d1d83396dfe39ce26e207787852876f09745282e6897497100b6d1eef9d4270c22c6891436358fd639f103d129f56a699f632342c00a387fda1f8d5c0/OA41%20ijstijden2.mp3',
'https://content.production.cdn.art19.com/validation=1588072233,dfc287f2-54ad-55bb-8764-7469848be7a5,TbYtG_B2iCCRo1MvybZ0ACMuE88/episodes/90b42ca3-1e2f-4095-8b15-0da56f320d86/77fdcf8c9ada551625f6c11ea3f0a785e946b8b972b83f9e002a20adc1f43ea7a51d939ab0dd1c8248dbbec859699d6057b1028d429b64f10fc0275a0ce72ee1/NRC%20Onbehaarde%20Apen%20%2312%20Het%20zelf.mp3']



for i, i_url in enumerate(download_mp3_list):
    file_name = os.path.basename(i_url)
    res = requests.get(i_url)
    print('Status code', res.status_code)
    if res.status_code == 200:
        with open('/home/bugger/Music/' + file_name, 'wb') as f:
            f.write(res.content)

    time.sleep(60)

# Onbehaarde apen
# download_mp3 = 'https://content.production.cdn.art19.com/validation=1587733954,11e708a5-1112-5785-ba99-865d48dfb25b,jug8R1rfO3DERVt-BjJL72ut5WI/episodes/11dddd02-e9c9-4f56-92b1-0309b7f0c07f/2b99cc9696c5a7c838fe6f7242e61548b6d10e477787d52dbb71bc0fcb7d81c79163d90a6ffeaeec472d59b22432c1abce51259e939a6041880ab6034afffb2d/%2390%3A%20Waar%20is%20alle%20antimaterie%20gebleven%3F.mp3'
# # download_mp3_list = ["https://rss.art19.com/episodes/bd537d3b-0b4d-4b95-b33f-acf6355d948e.mp3"]
#
# # Jordan Peterson
# # https://www.jordanbpeterson.com/podcast/s3-e2-biblical-series-genesis-1-chaos-order/
# download_mp3 = 'https://dcs.megaphone.fm/WWO7094747788.mp3?key=5d135a0edecec67785d9126c44ee21fc'
# download_mp3 = 'https://dcs.megaphone.fm/WWO6317272315.mp3?key=6b463d7fd933c26b12bb7cfb24dcc35d'

# onbeharde apen
# download_mp3_list = ["https://rss.art19.com/episodes/e33ce577-efcb-4de2-b1ef-f5977667123a.mp3",
# "https://rss.art19.com/episodes/c5a5605f-5259-4d48-93ee-8a5973fb7bdb.mp3",
# "https://rss.art19.com/episodes/9a6380aa-2d02-4054-bf3a-2eee7a0531a1.mp3",
# "https://rss.art19.com/episodes/586b9193-6a50-42cc-a3cc-56c9ccbe359f.mp3"]

# onbeharde apen
download_mp3_list = ["https://rss.art19.com/episodes/2ca2c11b-df9b-449a-a590-e132668b60a5.mp3",
                     "https://rss.art19.com/episodes/b4ceb473-89de-461b-8501-0a691909d34c.mp3",
                     "https://rss.art19.com/episodes/6611a2dc-bda0-47e9-ad15-ef12584ea649.mp3"]
download_mp3_list = ["https://d1ukfmmao1s9m3.cloudfront.net/dr1594565552000/002_College_1_Hoofdstuk_1_Inleiding__adeldom_dankzij_voorvaderen_of_door_eigen_verdiensten.mp3?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vZDF1a2ZtbWFvMXM5bTMuY2xvdWRmcm9udC5uZXQvZHIxNTk0NTY1NTUyMDAwLzAwMl9Db2xsZWdlXzFfSG9vZmRzdHVrXzFfSW5sZWlkaW5nX19hZGVsZG9tX2Rhbmt6aWpfdm9vcnZhZGVyZW5fb2ZfZG9vcl9laWdlbl92ZXJkaWVuc3Rlbi5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE2MTQwOTE5MDh9fX1dfQ__&Signature=XCgPC6lRr3ym3x5JyXIGtfKqjzmbnYxCgIXozWnGAxi86LdL5alWx0Msgtcmg7tPQN1dKlb3cgE2d-QahkbotyBWtft-UxxogJc-TeK91f959wRUH5w8fHCYO5tKdjsLCnKREDt0T9d3wHrmpjn8uKcBAsUsWw2FF-pcSBaBjkU_&Key-Pair-Id=APKAIKX2OHEK7X2QLNZA"]


for download_mp3 in download_mp3_list:
    file_name = os.path.basename(download_mp3)
    print(file_name)
    res = requests.get(download_mp3)
    print('Status code', res.status_code)
    file_name = file_name[:file_name.index('?')]
    if res.status_code == 200:
        with open('/home/bugger/Music/' + file_name, 'wb') as f:
            f.write(res.content)
    time.sleep(60)

# Get youtube mp3


import youtube_dl
import sys


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}
#  'preferredquality': '192',


if __name__ == "__main__":
    # filenames = 'https://www.youtube.com/watch?v=dNpILrLUvKs&list=PLscv4NA0bNSOWYDILwQPuXURMVkSaGuEU'
    # filenames = 'https://www.youtube.com/watch?v=IihEXA88GyI&list=RD12zcvCdtp4Q'
    # filenames = 'https://www.youtube.com/watch?v=IihEXA88GyI'
    # filenames = 'https://www.youtube.com/watch?v=ImllpvDwbQ8'
    # filenames = 'https://www.youtube.com/watch?v=jPeheoBa2_Y'
    # filenames = 'https://www.youtube.com/watch?v=mPymRFeTJa4'
    # filenames = 'https://www.youtube.com/watch?v=MqKVvaCN5M8&list=PLZqsyBiYZFQ3AGsUA-Y2uETjMxzAkyq8q'
    # filenames = 'https://www.youtube.com/watch?v=6cUdOo26YV8'
    # filenames = 'https://www.youtube.com/watch?v=TYFoQwL5HAw&list=PL10d-p2PLQ-JBId_a6ZPxYdDaeWDu5001'
    filenames = 'https://www.youtube.com/watch?v=nUBWUcSKBAc&list=PLcKCG4I2klHax42oaKlXyrlCl9iWI30od'
    filenames = 'https://www.youtube.com/watch?v=cD_vUV0n9vc&list=PLXNzhHCkUWiVeyPV-zt6W0K8QUMrJN9WA'
    filenames = 'https://www.youtube.com/watch?v=sWKDf6ggPjM&ab_channel=VrtRadio1'
    #
    filenames = 'https://www.youtube.com/watch?v=v55AH2_jhvk'
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([filenames])