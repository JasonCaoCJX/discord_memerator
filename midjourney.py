import requests
import json
import os

# load environment variables 
# from dotenv import load_dotenv
# load_dotenv()

mj_url = os.getenv('MJ_PROXY_URL')

class MJ():

  def subimt_image_api(self, prompt):
    # 设置请求头部
    headers = {'Content-Type': 'application/json'}

    # 发起POST请求
    data = {
      "base64Array": [],
      "notifyHook": "",
      "prompt": prompt,
      "state": "",
    }
    json_data = json.dumps(data)

    response = requests.post(f'{mj_url}/mj/submit/imagine',
                             headers=headers,
                             data=json_data)
    # print(response.text)

    # 获取响应内容
    result = json.loads(response.text)
    if result["code"] == 1:
      return result["result"]
    else:
      return None

  def upscale_image_api(self, index, task_id):
    # 设置请求头部
    headers = {'Content-Type': 'application/json'}

    # 发起POST请求
    data = {
      "action": "UPSCALE",
      "index": index,
      "notifyHook": "",
      "state": "",
      "taskId": task_id
    }
    json_data = json.dumps(data)

    response = requests.post(f'{mj_url}/mj/submit/change',
                             headers=headers,
                             data=json_data)
    # print(response.text)

    # 获取响应内容
    result = json.loads(response.text)
    if result["code"] == 1:
      return result["result"]
    elif result["code"] == 21:
      return result["result"]
    else:
      return None

  def check_progress_by_id(self, task_id):
    # 发起GEt请求
    response = requests.get(f'{mj_url}/mj/task/{task_id}/fetch')
    # print(response.text)
    result = json.loads(response.text)
    progress = result["progress"]
    status = result["status"]
    data = {"progress": progress, "imageUrl": "", "status": status}

    if (progress == "100%"):
      data["imageUrl"] = result["imageUrl"]
      data["status"] = "SUCCESS"
      return data
    else:
      return data
