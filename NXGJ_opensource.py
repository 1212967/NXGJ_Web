#By 1212967
#Python3
#希望学弟萌能用上））
import time
import json
import requests
from requests.packages import urllib3
import urllib.request
import sys
import json
import os
import subprocess
import requests
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
domain="."#必须配置！你访问时使用的地址 改成.可以自适应
openId="oWRkU0bGrAao9VZ-xTAQfH_mpFmw"#openID 请换成自己老师的
memid="5e2fadd261813532e3f1a852"#memberID 请换成自己的
def getTeacherDetail(openId, tid, cid):

    ts = int(round(time.time() * 1000))

    post = json.dumps({
        "_id": tid,
        "cid": cid,
        "daka_day": "",
        "teacher_cate": "teach_class_list",
        "member_id": "",
        "cls_ts": ts})

    headers = {
        "Host": "a.welife001.com",
        "Connection": "keep-alive",
        "Content-Length": "200",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "content-type": "application/json",
        "imprint": openId,
        "Referer": "https://servicewechat.com/wx23d8d7ea22039466/378/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    urllib3.disable_warnings()
    r = requests.post("https://a.welife001.com/notify/check4teacher",
                      headers=headers, data=post, verify=False)
    return r.text
def getTeacherInfo(openId):
    headers = {
        "Host": "a.welife001.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "content-type": "application/json",
        "imprint": openId,
        "Accept-Encoding": "gzip, deflate, br"
    }

    # f = open('data.txt','a+',encoding='utf-8')
    page = 0
    datas = []
    while True:
        urllib3.disable_warnings()
        r = requests.get("https://a.welife001.com/info/getParent?type=-1&members="+memid+"&page="+str(page) +"&size=10&date=-1&hasMore=true", headers=headers, verify=False)
        #print(r.text)
        data=r.text
        data=json.loads(data)
	#data = json.loads(data)
        '''if len(data['result']) == 0:
            break'''
        # f.write(str(data))
        datas.append(data)
        page = page + 1
        if(page == 5):#加载5页就退出，可以自行修改
            break

    # f.close()
    return datas
def getUserInfo(openId):

    headers = {
        "Host": "a.welife001.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "content-type": "application/json",
        "imprint": openId,
        "Referer": "https://servicewechat.com/wx23d8d7ea22039466/378/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }

    urllib3.disable_warnings()
    r = requests.get("https://a.welife001.com/getUser",
                     headers=headers, verify=False)

    print(r.text)


from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument('num','-1')
        api = self.get_argument('api','false')
        openurl = self.get_argument('openurl','false')
        num1 = self.get_argument('numf','0')
        num2 = self.get_argument('numl','0')
        teacherInfo = getTeacherInfo(openId)
        # 获取该教师的所有作业并写入
        i = 0
        projectList = {}
        tidList = []
        cidList = []
        nameList = []
        for eachPage in teacherInfo:
            for project in eachPage["data"]:
                if i==25:
                    break
                # 如果不是作业则跳过
                if project["type"] != 0:
                    continue
                if project["title"].find("班会作业")==-1 & project["title"].find("体育")==-1:
                    projectList[i] = project["title"] + \
                        "\n" + project["text_content"]
                    tidList.append(project["_id"])
                    cidList.append(project["cls"])
                    nameList.append(project["title"])
                    i = i + 1
        if(api=="true" and num=="-1" and openurl!="true"):
             while (True):
                self.write("项目列表:<br>")
                self.write("-----------------------------------------------<br>")
                for key, value in projectList.items():
                    self.write('{key}. {value}<br>'.format(key=key, value=value))
                    self.write("-----------------------------------------------<br>")
                break
        if(api!="true" and num=="-1"  and openurl!="true"):
            self.write("<!DOCTYPE html><html lang=\"en\"><head ><meta charset=\"UTF-8\"><title>NXGJ</title><script type=\"text/javascript\" src=\"http://apps.bdimg.com/libs/jquery/1.9.1/jquery.min.js\"></script><link type=\"text/css\" rel=\"stylesheet\" href=\"https://1212967.xyz/xgj/web/css.css\"></head><body style=\"background-color: rgba(204,204,204,0.23)\"><div class=\"fav_list\"><div  class=\"fav_list_box\"><div  class=\"fav_list_title\"><h3 class=\"fav_list_title_h3\">作业列表</h3><div class=\"fav_num\"><span >NXGJ_Web 1.1</span></div></div><div  class=\"my_fav_con\"><div><ul  class=\"my_fav_list\">")
            while (True):
                for key, value in projectList.items():
                    self.write("<li class=\"my_fav_list_li\" id=\"\"><a  class=\"my_fav_list_a\" href=\""+domain+"/?num={key}\" target=\"_blank\">".format(key=key, value=value))
                    self.write('{key}. {value}<br>'.format(key=key, value=value))
                    self.write("</a><label class=\"my_fav_list_label\"><!--<span >2019-04-08</span>--><a href=\""+domain+"/?num={key}\" class=\"cancel_fav\"><em>打开</em></a></label></li>".format(key=key, value=value))
                break
            self.write("</ul></div></div></div></div></body></html>")
        if(api=="true" and num!="-1" and openurl!="true"):
            self.write("->NXGJ_Web 1.1<br>")
            self.write("->time:")
            self.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            self.write("<br>->note:解析成功，下方链接即为图片链接<br><br>")
            choose = int(num)
            # 加载作业
            tid = tidList[choose]
            cid = cidList[choose]

            teacherDetail = getTeacherDetail(openId, tid, cid)
            teacherDetail = json.loads(teacherDetail)
            membersMap = teacherDetail['membersMap']
            feedBacks = teacherDetail['accepts']
            for eachFeedback in feedBacks:
                studentId = eachFeedback['member']
                feedBackPhoto = eachFeedback['feedback_photo']
                ret = membersMap[studentId]['name'] + '\n'
                self.write(ret)
                self.write("<br>")
                for photo in feedBackPhoto:
                    url = "http://img.welife001.com/"
                    photoUrl = url + photo
                    self.write(photoUrl)
                    self.write("<br>")
                self.write("<br>-----------------------------------------------<br>")
        if(api!="true" and num!="-1" and openurl!="true"):
            numf=0
            numl=0
            self.write("<!DOCTYPE html><html lang=\"en\"><head ><meta charset=\"UTF-8\"><title>NXGJ</title><script type=\"text/javascript\" src=\"http://apps.bdimg.com/libs/jquery/1.9.1/jquery.min.js\"></script> <link type=\"text/css\" rel=\"stylesheet\" href=\"https://1212967.xyz/xgj/web/css.css\"></head><body style=\"background-color: rgba(204,204,204,0.23)\"><div class=\"fav_list\"><div  class=\"fav_list_box\"><div  class=\"fav_list_title\"><h3 class=\"fav_list_title_h3\">答案列表</h3><div class=\"fav_num\"><span >NXGJ_Web 1.1</span></div></div><div  class=\"my_fav_con\"><div><ul  class=\"my_fav_list\">")
            choose = int(num)
            # 加载作业
            tid = tidList[choose]
            cid = cidList[choose]

            teacherDetail = getTeacherDetail(openId, tid, cid)
            teacherDetail = json.loads(teacherDetail)
            membersMap = teacherDetail['membersMap']
            feedBacks = teacherDetail['accepts']
            for eachFeedback in feedBacks:
                studentId = eachFeedback['member']
                feedBackPhoto = eachFeedback['feedback_photo']
                ret = membersMap[studentId]['name'] + '\n'
                self.write("<li class=\"my_fav_list_li\" id=\"\"><p  class=\"my_fav_list_a\" >")
                self.write(ret)
                self.write("<br><br>")
                for photo in feedBackPhoto:
                    url = "http://img.welife001.com/"
                    photoUrl = url + photo
                    self.write(photoUrl)
                    self.write("<br>")
                    numl=numl+1
                self.write("</p><label class=\"my_fav_list_label\"><!--<span >2019-04-08</span>--><a href=\""+domain+"/?num="+num+"&openurl=true&numf=%d"%numf+"&numl=%d"%numl+"\" class=\"cancel_fav\"><em>一键全部打开</em></a></label></li>")
                numf=numl+1
        if(openurl=="true"):
            numn=1
            choose = int(num)
            # 加载作业
            tid = tidList[choose]
            cid = cidList[choose]

            teacherDetail = getTeacherDetail(openId, tid, cid)
            teacherDetail = json.loads(teacherDetail)
            membersMap = teacherDetail['membersMap']
            feedBacks = teacherDetail['accepts']
            self.write("<html><script type=\"text/javascript\">function sleep(ms){return new Promise(resolve => setTimeout(resolve,ms));}async function load(){")
            for eachFeedback in feedBacks:
                studentId = eachFeedback['member']
                feedBackPhoto = eachFeedback['feedback_photo']
                for photo in feedBackPhoto:
                    url = "http://img.welife001.com/"
                    photoUrl = url + photo
                    if(numn>=int(num1) and numn<=int(num2)):
                        self.write("window.open(\""+photoUrl+"\");await sleep(300);")
                    numn=numn+1
            self.write("}</script><body onload=\"load();\"></body></html>")
        ip=self.request.headers.get("cf-connecting-ip","")#请自行更改IP获取方式
        ua=self.request.headers.get("user_agent","")
        print("-----\nIP:"+ip)
        with open("NXGJ_log.txt","a+") as f:#访问IP记录
            f.write("IP："+ip+"\n")
            f.write("时间："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n")
            f.write("---------------\n")

            
if __name__ == "__main__":
    print("NXGJ Server is running")
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

