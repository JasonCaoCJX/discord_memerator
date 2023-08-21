from PIL import Image, ImageFont, ImageDraw
import urllib.request
import textwrap
import time
import re
import os


def splice_text_image(user_id, url, top, bottom):
  timestamp = int(time.time())
  filename = str(user_id) + "-" + str(timestamp)

  # 添加头部信息
  cjopenx = urllib.request.build_opener()
  cjopenx.addheaders = [('User-Agent', 'Mozilla/5.0')]
  urllib.request.install_opener(cjopenx)

  # 加载网络图片
  req = urllib.request.urlopen(url)
  img = Image.open(req)

  # 定义画布及字体
  font_size = 70
  stroke_width = 8
  Draw = ImageDraw.Draw(img)
  Font = ImageFont.truetype("simheibd.ttf", font_size, encoding="utf-8")

  # 在图片上下方添加文字
  draw_text(Draw, Font, img, top, "top", font_size, stroke_width)
  draw_text(Draw, Font, img, bottom, "bottom", font_size, stroke_width)

  output_dir = 'output/'
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # 导出图片为文件
  img.save(f"output/{filename}.jpg")
  return f"output/{filename}.jpg"


def draw_text(Draw, Font, img, text, position, font_size, stroke_width):
  font_size = font_size + stroke_width * 2
  image_width, image_height = img.size

  wrapper_width = int((image_width - 50) / font_size)
  if (check_language(text) != "zh"):
    wrapper_width *= 2
  # 自动换行
  wrapper = textwrap.TextWrapper(width=wrapper_width)

  lines = wrapper.wrap(text=text)
  # print(lines)

  # 首行绘制高度
  draw_height = 50
  if position == "top":
    draw_height = 50
  else:
    draw_height = int(
      (image_height - (len(lines) * (font_size - stroke_width)) - 30))

  # 逐行绘制文字
  for line in lines:
    line_width = Font.font.getsize(line)[0][0]
    text_coordinate = int((image_width - line_width) / 2), draw_height

    # 绘制描边
    Draw.text(text_coordinate,
              line, (0, 0, 0),
              font=Font,
              stroke_width=stroke_width,
              stroke_fill=(0, 0, 0, 255))
    # 绘制字体
    Draw.text(text_coordinate, line, (255, 255, 255), font=Font)

    # Draw.text(text_coordinate, line, (255, 255, 255), font=Font)

    draw_height += font_size - stroke_width


def check_language(string):
  pattern = re.compile(r'^[\u4e00-\u9fa5a-zA-Z]+$')
  if re.match(pattern, string):
    if re.match(r'^[\u4e00-\u9fa5]+$', string):
      return 'zh'
    else:
      return 'en'
  else:
    return 'mix'
