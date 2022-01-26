#azure
import requests,json,urllib.request,os
from PIL import Image,ImageDraw,ImageFont

# 顔認識させる画像のURL
image_url = 'https://www.foto.ne.jp/user_data/packages/stockfoto2/img/selection/top_sl_jyosei.jpg'

def hantei(url):
    # サブスクリプションキー設定
    subscription_key = "7424afc9348543b59f18366182f5fc12"
    assert subscription_key

    # エンドポイントURL設定
    face_api_url = "https://webchat.cognitiveservices.azure.com/face/v1.0/detect"

    # ヘッダ設定
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    # パラメーターの設定
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # POSTリクエスト
    request = requests.post(face_api_url, params=params,
        headers=headers, json={"url": image_url})

    print(request)
    # JSONデコード
    response = request.json()

    # URLの画像保存
    image_path = os.path.join(os.path.join(os.path.join(os.environ.get("HOME")), 'Desktop/hackson'),'myPicture.png')
    urllib.request.urlretrieve(image_url,image_path)

    # 顔と認識された箇所に四角を描く関数
    def draw_rectangle( draw, coordinates, color,smile ,width = 1):
        flag=False
        if smile>0.0:
            flag=True
        if flag:
            for i in range(width):
                rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
                rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)

                draw.rectangle((rect_start, rect_end), outline = color)

    # 顔と認識された箇所に性別を描く関数
    def draw_smile(draw, coordinates, smile, align, font, fill):
        draw.text(coordinates, str(smile), align = align,font = font, fill = fill)

    # イメージオブジェクト生成
    im = Image.open(image_path)
    drawing = ImageDraw.Draw(im)

    hantei = []

    for index in range(len(response)):
        # 取得した顔情報
        image_top    = response[index]['faceRectangle']['top']
        image_left   = response[index]['faceRectangle']['left']
        image_height = response[index]['faceRectangle']['height']
        image_width  = response[index]['faceRectangle']['width']
        image_smile = response[index]['faceAttributes']['smile']
        hantei.append(image_smile)
        #print(response[index]["faceAttributes"])

        # 関数呼び出し(四角)
        face_top_left = (image_left, image_top)
        face_bottom_right = (image_left + image_width, image_top + image_height)
        outline_width = 10
        outline_color = "Blue"
        draw_rectangle(drawing, (face_top_left, face_bottom_right), color = outline_color,smile=image_smile, width = outline_width)

        # 関数呼び出し(smile)
        gender_top_left = (image_left, image_top - 100)
        font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 100)
        align = 'Left'
        fill  = 'Red'
        draw_smile(drawing, gender_top_left,image_smile,align, font, fill)

    sm=0
    for i in hantei:
        if i >=0.5:
            sm=1
            break
    if sm==1:return 1
    else:return 0

hantei(image_url)