import scrapy
from urllib import request
# from PIL import Image
import sys
sys.path.append("..")


class DoubanLoginSpiderSpider(scrapy.Spider):
    name = 'douban_login_spider'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login'] # 这个地方从登录的url开始写
    login_url = 'https://accounts.douban.com/login'

    def parse(self, response):
        data = {
            'source': 'None',
            'redir': 'https://www.douban.com/',
            'form_email': '',# 这里输入你的账号
            'form_password': '', # 这里输入你的密码
            'remember': 'on',
            'login': '登录',
        }
        captcha_image = response.xpath('//img[@id="captcha_image"]/@src').get()
        print('='*50)
        # 豆瓣在输入错误几次才会出现验证码，这里加一个判断，如果没有出现验证码直接提交表单登录
        if captcha_image:
            captcha = self.regonize_captgha(captcha_image)
            data['captcha-solution: '] = captcha # 把验证码放入data中
            captcha_id = response.xpath('//input[@name=captcha-id]/@value').get()
            data['captcha_id'] = captcha_id # 把这个id也放进去
        # 执行登录操作，提交表单，执行回调解析登录后的页面。
        yield scrapy.FormRequest(url=self.login_url,formdata=data,callback=self.parse_page)

    def parse_page(self,response):
        if response.url == 'https://www.douban.com/':
            print('登录成功')
        else:
            print('登录失败')
        # 这里是修改个人信息的页面，我们跳转过去修改一下信息
        url = 'https://www.douban.com/people/184751170/'
        yield scrapy.Request(url=url,callback=self.xiugai)

    # 修改个人信息
    def xiugai(self,response):
        # 这里也是一个post请求，查找提交的参数，url。完成登录。
        ck = response.xpath('//input[@name="ck"]/@value').get()
        data = {'ck':ck,
            'signature': '云游十方'}
        edit_url = 'https://www.douban.com/j/people/184751170/edit_signature'
        # 这里提交表单以修改个人信息，同时指定callcake，如果不指定scrapy会默认调用parse方法。
        yield scrapy.FormRequest(url=edit_url,formdata=data,callback=self.parse_none)

    def parse_none(self,response):
        pass


    # 识别验证码，人工识别 也可以以人工打码的方式识别，在这里做扩展
    def regonize_captgha(self,captcha_img):
        request.urlretrieve(captcha_img,'captcha.png') # 把验证码保存到本地
        image = Image.open('captcha.png') # y用image库的open方法打开图片
        image.show() # 用show方法展现在窗口中
        captcha = input('请输入验证码：') # 手动输入验证码以完成登录
        return captcha
