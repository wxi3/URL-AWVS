import requests
import re
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


apikey = 'input yourself api in here'#API
headers = {'Content-Type': 'application/json',"X-Auth": apikey}

def get_titles():
    urls = open('urls.txt','r')
    for url1 in urls:
        url = url1.strip()
        try:
            html = requests.get(url,timeout=3)
            status = html.status_code
            try:
                if status == 200:
                    html.encoding = 'utf-8'
                    content = html.text
                    title = re.findall('<title>(.*)</title>', content)[0]
                    print(url,status,title)
                    with open("url.txt",'a') as f:
                        f.write(url + '\n')
                else:
                    print(url,status)
            except Exception as e:
                print("Something Have Error")
        except:
            print(url + " is die")
    urls.close()



def addTask(url,target):
    try:
        url = ''.join((url, '/api/v1/targets/add'))
        data = {"targets":[{"address": target,"description":""}],"groups":[]}
        r = requests.post(url, headers=headers, data=json.dumps(data), timeout=30, verify=False)
        result = json.loads(r.content.decode())
        return result['targets'][0]['target_id']
    except Exception as e:
        return e
def scan(url,target,Crawl,user_agent,profile_id,proxy_address,proxy_port):
    scanUrl = ''.join((url, '/api/v1/scans'))
    target_id = addTask(url,target)

    if target_id:
        data = {"target_id": target_id, "profile_id": profile_id, "incremental": False, "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
        try:
            configuration(url,target_id,proxy_address,proxy_port,Crawl,user_agent)
            response = requests.post(scanUrl, data=json.dumps(data), headers=headers, timeout=30, verify=False)
            result = json.loads(response.content)
            return result['target_id']
        except Exception as e:
            print(e)

def configuration(url,target_id,proxy_address,proxy_port,Crawl,user_agent):
    configuration_url = ''.join((url,'/api/v1/targets/{0}/configuration'.format(target_id)))
    data = {"scan_speed":"fast","login":{"kind":"none"},"ssh_credentials":{"kind":"none"},"sensor": False,"user_agent": user_agent,"case_sensitive":"auto","limit_crawler_scope": True,"excluded_paths":[],"authentication":{"enabled": False},"proxy":{"enabled": Crawl,"protocol":"http","address":proxy_address,"port":proxy_port},"technologies":[],"custom_headers":[],"custom_cookies":[],"debug":False,"client_certificate_password":"","issue_tracker_id":"","excluded_hours_id":""}
    r = requests.patch(url=configuration_url,data=json.dumps(data), headers=headers, timeout=30, verify=False)
def main():
    Crawl = False
    proxy_address = '127.0.0.1'
    proxy_port = '8080'
    awvs_url = 'https://localhost:3443' #awvs url
    with open('url.txt','r',encoding='utf-8') as f:
        targets = f.readlines()
    profile_id = "11111111-1111-1111-1111-111111111111"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21" #扫描默认UA头
    if Crawl:
        profile_id = "11111111-1111-1111-1111-111111111117"
    for target in targets:
        target = target.strip()
        if scan(awvs_url,target,Crawl,user_agent,profile_id,proxy_address,int(proxy_port)):
            print("{0} 添加成功".format(target))

if __name__ == '__main__':
    get_titles()
    main()
