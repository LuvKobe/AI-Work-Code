import base64
import urllib
import requests
from openai import OpenAI

# 百度 API 相关信息
API_KEY = "EDW2XiaglULR0PG3orsSNzif"
SECRET_KEY = "WhG9G7LO670x9OCQg0tnsCCjnHG9fnrt"

# 通义千问 API 相关信息
API_KEY_QWEN = "sk-c974b2e438244ecb8cebaad3c975ab6d"
BASE_URL_QWEN = "https://dashscope.aliyuncs.com/compatible-mode/v1"


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件 base64 编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行 urlencoded
    :return: base64 编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是 None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def recognize_image(image_path):
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + get_access_token()
    image_base64 = get_file_content_as_base64(image_path, True)
    if image_base64 is None:
        return False
    payload = f"image={image_base64}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        response.raise_for_status()
        result = response.json()
        for item in result.get('result', []):
            if ('鹦鹉' in item.get('keyword', '') or '鹦鹉' in item.get('name', '')) and item.get('score', 0) > 0.5:
                return True
    except requests.RequestException as e:
        print(f"请求百度图像识别 API 时出错: {e}")
    return False


def interact_with_qwen():
    client = OpenAI(
        api_key=API_KEY_QWEN,
        base_url=BASE_URL_QWEN
    )
    messages = [
        {"role": "system", "content": "你是一只鹦鹉，同时兼任低龄儿童英语教师，使用中英双语与孩子互动。"}
    ]
    print("开始与鹦鹉老师互动啦！输入 '退出' 结束对话。")
    while True:
        user_input = input("你: ")
        if user_input.lower() == '退出':
            break
        messages.append({"role": "user", "content": user_input})
        try:
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=messages
            )
            assistant_response = completion.choices[0].message.content
            print(f"鹦鹉老师: {assistant_response}")
            messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            print(f"与通义千问交互时出错: {e}")


def main(image_path):
    if recognize_image(image_path):
        interact_with_qwen()
    else:
        print("图片中没有置信度大于 0.5 的鹦鹉。")


if __name__ == '__main__':
    image_path = "/root/Nlp_demo/Bird.jpg"
    main(image_path)
    