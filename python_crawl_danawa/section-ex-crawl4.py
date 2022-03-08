import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By # 언제까지
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # 상태 예상
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from io import BytesIO
from fake_useragent import UserAgent
import xlsxwriter
from PIL import Image


ua = UserAgent(verify_ssl=False)
url = 'http://www.danawa.com/?src=adwords&kw=GA0000020&gclid=Cj0KCQjw8p2MBhCiARIsADDUFVHaf4jlvVcaIwFKStgBcSjC1zp6iGSSUlJXjcUuyicazWkA7Z94IZwaAny8EALw_wcB'
request_headers = {
    'User-Agent': ua.random,
    'Referer': url
}


chrome_options = Options()
chrome_options.add_argument("--headless")

workbook = xlsxwriter.Workbook('C:/crawling_result.xlsx')


worksheet = workbook.add_worksheet()


browser = webdriver.Chrome('./webdriver/chromedriver.exe') 

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

browser.set_window_size(1920, 1280) # maximize_window(), minimize_window() 함수로 최대와 최소 설정 가능

# 페이지 이동
browser.get('http://prod.danawa.com/list/?cate=112758&15main_11_02') # 그때그때 개발자 도구 확인하면서 바꿔가야 함

# 1차 페이지 내용
#print('Before Page Contents : {}'.format(browser.page_source))

WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'))).click()


# browser.find_element_by_xpath('//*[@id="dlMaker_simple"]/dd/div[2]/button[1]').click()
# 되긴 하는데 위에 것이 더 정확함


WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectMaker_simple_priceCompare_A"]/li[16]/label'))).click()

# 2차 페이지 내용
# print('After Page Contents : {}'.format(browser.page_source))

time.sleep(2)

# 현재 페이지
cur_page = 1

# 크롤링 페이지 수
target_crawl_num = 5
ins_cnt = 1
while cur_page <= target_crawl_num:
    # bs4 초기화
    soup = BeautifulSoup(browser.page_source,'html.parser')


    pro_list = soup.select('li.prod_item.prod_layer')
    print('\n'*5)

    # 페이지 번호 출력
    print('***** Current Page : {}'.format(cur_page),'*****')


    pro_list.pop()

    for v in pro_list:
        # 임시 출력
        # print(v)
        if not v.find('div', class_='ad_header'):
            print(ins_cnt)
            prod_name = v.select('p.prod_name > a')[0].text.strip()
            print(prod_name)
            # print(v.select('p.prod_name > a')[0].text.strip())
            prod_price = v.select('p.price_sect > a')[0].text.strip()
            print(prod_price)
            
# print(v.select('a.thumb_link > img')[0]['data-original'])
# print(v.select('a.thumb_link > img')[0]['src'])
            
            # if v.select('a.thumb_link > img')[0].attrs.get('data-original'):
            #     print(v.select('a.thumb_link > img')[0].attrs)
            #     img_data = BytesIO(req.urlopen('https:'+ v.select('a.thumb_link > img')[0]['data-original']).read())
            # else:
            #     print(v.select('a.thumb_link > img')[0]['src'])
            #     img_data = BytesIO(req.urlopen('https:'+ v.select('a.thumb_link > img')[0]['src']).read())
            try:
                if v.select('a.thumb_link > img')[0].attrs.get('data-original'):
                    #print(v.select('a.thumb_link > img')[0].attrs)
                    # time.sleep(0.1)
                    img_data = (BytesIO(requests.get('https:'+v.select('a.thumb_link > img')[0]['data-original'], headers=request_headers).content))
                    Image.open(img_data).save('./resource/다나와/pc{}.png'.format(ins_cnt))
                  
                else:
                    img_data = (BytesIO(requests.get('https:'+v.select('a.thumb_link > img')[0]['src'], headers=request_headers).content))   
                    Image.open(img_data).save('./resource/다나와/pc{}.png'.format(ins_cnt))
               

                # 엑셀 저장 (텍스트)    
                worksheet.write('A%s'% ins_cnt, prod_name)
                worksheet.write('B%s'% ins_cnt, prod_price)
                
                # 엑셀 저장 (이미지)
                prod_save_name = prod_name + '.png'
                worksheet.insert_image('C%s'% ins_cnt, prod_name, {'image_data': img_data}) # 첫번째 인수 위치, 2번째 이름, 3번째 딕셔너리 형태로 키 고정, 값 BytesIo           

                ins_cnt += 1
            except Exception as e:
                print('error : {}'.format(e))
            # print(img_data)
            # 이미지 요청 후 바이트 변환
            
            # print(v.select('p.price_sect > a')[0].text.strip())
            
            # 이 부분에서 엑셀 저장(파일, db 등)


        print()
    print() # 페이지 바뀔 때 마다
    

    # 페이지 별 스크린 샷 저장
    # browser.save_screenshot('C:/target_page{}.png'.format(cur_page))

    # 페이지 증가
    cur_page += 1

    if cur_page > target_crawl_num:
        print('Crawling Succeed')
        break

    # 페이지 이동 클릭

    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.number_wrap > a:nth-child({})'.format(cur_page)))).click() 

    # BeautifulSoup 인스턴스 삭제 # 필요없는 인스턴스 삭제, 자바나 파이썬은 가비지 컬렉터가 삭제하지만 그 전에 힙 영역 낭비 줄이기
    del soup

    # 3초간 대기
    time.sleep(3)


# 행 열 너비 조절
worksheet.set_column(0,0,35)
worksheet.set_column(1,1,12)
worksheet.set_column(2,2,25)

for i in range(150):
    worksheet.set_row(i,80)
# 브루우저 종료
browser.quit()

# 엑셀 파일 닫기
workbook.close()