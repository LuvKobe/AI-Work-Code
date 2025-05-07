import base64
import urllib
import requests

API_KEY = "EDW2XiaglULR0PG3orsSNzif"
SECRET_KEY = "WhG9G7LO670x9OCQg0tnsCCjnHG9fnrt"

def main():
        
    url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token=" + get_access_token()
    
    # image 可以通过 get_file_content_as_base64("C:\fakepath\Bird.jpg",True) 方法获取
    # D:\00Edison\01_studyCode\NLP_demo_py
    image_base64 = get_file_content_as_base64("/root/Nlp_demo/test.jpg", True)
    if image_base64 is None:
        return
    # 设置 payload
    payload = f"image={image_base64}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    print(response.text)
    

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
