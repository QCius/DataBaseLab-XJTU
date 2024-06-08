import requests
import json
import csv

# 目标URL
url = "https://ehall.xjtu.edu.cn/jwapp/sys/kcbcx/modules/qxkcb/qxfbkccx.do"

# 进入全校课表界面，按F12，进入网络栏，点击保留日志，点击下一页，填充下面的请求头
# 请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "EMAP_LANG=zh; THEME=cherry; _WEU=PQMQI7Z4H1Hxk1bxKjPyeLCkH3vjhq6Rwg5K4XHUL9hHkfufm9llNxOOv1HSIDNEOi6SpgoA6ZlZw0tC7SoLC6zfvFNdV1l54ILNG76ebKO8YsTxxE3lO9FGXv6pAritzwO3jha9NaXcgvDI8WXVge2xuts0xuuPNbb1IZud6ks.; _ga=GA1.3.1533209884.1693810680; _ga_X1H9BHPE93=GS1.3.1693810680.1.0.1693810680.0.0.0; UM_distinctid=18c9ec36bfb8cf-09850fb3dd71c8-4c657b58-1fa400-18c9ec36bfc1433; route=ab22dc972e174017d573ee90262bcc96; CASTGC=dT49rqIKJPiuKaU53+oDXNimnpxv/6RTnZ5DBKUwDjsgEF6tPITB1Q==; MOD_AMP_AUTH=MOD_AMP_a835fab8-88ab-4c0e-9a53-fe4609932af0; asessionid=b80c1056-5909-46ea-978f-3d2a30510178; amp.locale=undefined; JSESSIONID=S9fdPEkjibjEpTqSvNf-3kN16uhqFRQI3vi9oGZZQRY5EASBXvRF!-685311190",
    "Origin": "https://ehall.xjtu.edu.cn",
    "Referer": "https://ehall.xjtu.edu.cn/jwapp/sys/kcbcx/*default/index.do?amp_sec_version_=1&gid_=S0dyeFZ1TW5DSzBJNzI1MXdDc0FQM29tN2JTNGltWDhkOW16TEUzVDd2TWRlWDNVcUY1T1ZVNXdSMjMrTmdaMGhZTEFRdWdmSytLdGtqQldmTjJKeUE9PQ&EMAP_LANG=zh&THEME=cherry"
}

courses_id = {}

# 请求数据
def request_data(page_number):
    data = {
        "pageSize": 100,
        "pageNumber": page_number,
        "querySetting": json.dumps([
            {"name": "XNXQDM", "value": "2023-2024-2", "linkOpt": "and", "builder": "equal"},
            [
                {"name": "RWZTDM", "value": "1", "linkOpt": "and", "builder": "equal"},
                {"name": "RWZTDM", "linkOpt": "or", "builder": "isNull"}
            ]
        ]),
        "*order": "+KKDWDM,+KCH,+KXH"
    }
    return data

# 发送POST请求
def post_request(n):
    with open('C:/Users/Jiefucious/Desktop/course.csv', 'w',newline='') as csvfile:
        fieldnames = ['C#', 'CNAME', 'PERIOD', 'CREDIT', 'TEACHER']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() 

        for i in range(n):
            response = requests.post(url, headers=headers, data= request_data(i))
            print("响应状态码：", response.status_code)
            #print("响应头：", response.headers)
            #print("响应内容：", response.text)

            # 解析JSON响应
            if response.status_code == 200:
    
                try:
                    json_data = response.json()
                    for course in json_data.get('datas', {}).get('qxfbkccx', {}).get('rows', []):
                        original_course_id = course.get('KCH')
                        if original_course_id[:4] == "COMP":
                            course_id = f"CS-{original_course_id[-4:]}"
                        elif original_course_id[:2] == "ELEC":
                            course_id = f"EE-{original_course_id[-4:]}"
                        else:
                            course_id = original_course_id
                        if course_id in courses_id:
                            continue
                        course_info = {
                            'C#': course_id,
                            'CNAME': course.get('KCM'),
                            'PERIOD': course.get('XS'),
                            'CREDIT': course.get('XF'),
                            'TEACHER': course.get('SKJS')
                        }
                        courses_id[course_id] = 1            
                        writer.writerow(course_info)
                        print(course_info)
                
                except requests.exceptions.JSONDecodeError as e:
                    print("JSON解码错误:", e)
            else:
                print(f"请求失败，状态码：{response.status_code}")


if __name__ == '__main__':
    post_request(300)

