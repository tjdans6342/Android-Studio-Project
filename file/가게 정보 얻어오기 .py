no_image_url = 'url 없음'

from pickletools import read_unicodestring8
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
# import pyautogui
# import pyperclip
import copy

# return_work_time
def return_work_time(we, he):
    weeks = ['월', '화', '수', '목', '금', '토', '일']
    we_text = [w.text for w in we]
    he_text = [h.text for h in he]

    # case1. 매일인 경우 처리
    if we_text[0] == '매일':
        we_text = weeks
        he_text = he_text * 7

    # case2. 설명인 경우 처리
    for i, h in enumerate(he_text):
        for u in ['휴무', '쉬는', '휴업']:
            if u in h:
                he_text[i] = '휴무일'
        if '없음' in h:
            he_text[i] = '정보없음'
            
    # 월요일 기준으로 정렬
    temp_we_text = copy.deepcopy(we_text)
    temp_he_text = copy.deepcopy(he_text)

    for i, w in enumerate(we_text):
        if w == '월':
            monday_idx = i;

    for i in range(7):
        we_text[i] = temp_we_text[monday_idx % 7]
        he_text[i] = temp_he_text[monday_idx % 7]
        monday_idx = (monday_idx + 1) % 7

    output = '\n'.join([w + ' ' + h[:(h.find('\n') if '\n' in h else len(h))] for w, h in zip(we_text, he_text)])
    
    return output


# return_coordinate
def return_coordinate(addr):
    driver2 = webdriver.Chrome("C:/Users/Gliver/Desktop/chromedriver.exe", options=chrome_options)
    # driver2 = webdriver.Chrome(service=service, options=chrome_options)
    driver2.implicitly_wait(5)
    driver2.get('https://address.dawul.co.kr/')
    time.sleep(2)

    # 팝업창 닫기
    driver2.switch_to.window(driver2.window_handles[1])
    time.sleep(1)
    driver2.close()
    time.sleep(1)
    driver2.switch_to.window(driver2.window_handles[0])
    time.sleep(2)
    
    # 위도, 경도 찾기
    search_box = driver2.find_element(By.CSS_SELECTOR, ".juso")
    search_box.clear()
    search_box.send_keys(addr)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    
    coordinate = driver2.find_element(By.CSS_SELECTOR, '#insert_data_5').text
    latitude, longitude = [u[3:] for u in coordinate.split(', ')]

    driver2.close()
    del driver2
    return latitude, longitude



foods = ['라면', '초밥', '회', '연어', '우동', '카레', '짜장면', '짬뽕', '마라탕', '탕수육', '떡볶이', '김밥']

for food in foods:
    # 초기 세팅
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome("C:/Users/Gliver/Desktop/chromedriver.exe", options=chrome_options)
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()

    # 네이버 지도로 이동
    url = 'https://map.naver.com/'
    driver.get(url)
    time.sleep(1)

    # 네이버 지도에 해당 음식점 검색
    # food = '해장국'
    search_input = driver.find_element(By.CSS_SELECTOR, '.input_search.ng-pristine')
    search_input.click()
    search_input.send_keys(f'전북대 {food}')
    search_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # 가게 목록으로 frame 전환
    frame = driver.find_element(By.CSS_SELECTOR, 'iframe#searchIframe')
    driver.switch_to.frame(frame)
    time.sleep(1)

    # 스크롤 down을 통해서 가게 정보 불러오기
    for i in range(3):
        scroll_div = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]')
        driver.execute_script(f'arguments[0].scrollBy(0, 1000)', scroll_div)
        time.sleep(0.3)

            


    names = []
    classifications = []
    image_urls = []

    addresses = []
    ranks = []
    work_times = []
    phone_numbers = []

    latitudes = []
    longitudes = []


    # 가게들 정보 불러오기
    # elements = driver.find_elements(By.CSS_SELECTOR, 'li._22p-O._2NEjP')
    elements = driver.find_elements(By.CSS_SELECTOR, 'li.VLTHu.OW9LQ')
    print(len(elements))

    # 가게 정보 하나씩 크롤링하기
    for idx, element in enumerate(elements, 1):
        # 가게 이름
        name = element.find_element(By.CSS_SELECTOR, '.place_bluelink').text
        # 가게 분류
        classification = element.find_element(By.CSS_SELECTOR, '.YzBgS').text
        # 이미지 링크
        try:
            image_url = element.find_element(By.CSS_SELECTOR, '.lazyload-wrapper > img').get_attribute('src')
        except:
            image_url = no_image_url # no_image_url 쓸 거임

        print(name)

        # 가게 이름 버튼 클릭
        name_btn = element.find_element(By.CSS_SELECTOR, '.place_bluelink')
        name_btn.click()
        time.sleep(2)


        # 가게 상세정보로 frame 전환
        driver.switch_to.default_content() # 본래 frame으로 갔다가 해야 함!
        info_frame = driver.find_element(By.CSS_SELECTOR, 'iframe#entryIframe')
        driver.switch_to.frame(info_frame)


        # 가게 정보(평점) 크롤링1
        try: rank = driver.find_element(By.CSS_SELECTOR, '.PXMot > em').text
        except: rank = 'rank 없음'
        # 가게 정보(전화번호) 크롤링2
        try: phone_number = driver.find_element(By.CSS_SELECTOR, '.x8JmK > .dry01').text
        except: phone_number = 'phone_number 없음'
        # 가게 정보(주소) 크롤링3
        try: address = driver.find_element(By.CSS_SELECTOR, 'span.IH7VW').text
        except: address = 'address 없음'
        # 가게 정보(영업시간) 크롤링4
        try:
            driver.find_element(By.CSS_SELECTOR, '.X007O').click()
            time.sleep(1)
            week_elements = driver.find_elements(By.CSS_SELECTOR, '.kGc0c')
            hour_elements = driver.find_elements(By.CSS_SELECTOR, '.qo7A2')
            work_time = return_work_time(week_elements, hour_elements)
        except: 
            work_time = '영업시간 정보 없음'
        
        # 가게 정보(위도, 경도) 크롤링5
        try:
            latitude, longitude = return_coordinate(address)
        except:
            latitude, longitude = -1, -1

        # 상세정보 닫기 버튼 클릭
        driver.switch_to.default_content() # 본래 frame으로 갔다가 해야 함!
        close_btn = driver.find_element(By.CSS_SELECTOR, '.btn_entry_close')
        close_btn.click()
        time.sleep(1)

        # 다시 가게 목록으로 frame 전환
        driver.switch_to.frame(frame)


        # 크롤링한 가게 정보 출력
        print(f'[{idx} 번째 가게] {"-" * 220}')
        print(f'가게 이름: {name}')
        print(f'가게 주소: {address}')
        print(f'가게 분류: {classification}')
        print(f'가게 평점: {rank}')
        print(f'가게 전화번호: {phone_number}')
        print(f'가게 이미지 url: {image_url}\n')
        print(f'위도: {latitude}')
        print(f'경도: {longitude}\n')
        print(f'[가게 영업시간]\n{work_time}')
        print()

        names.append(name)
        addresses.append(address)
        classifications.append(classification)
        ranks.append(rank)
        phone_numbers.append(phone_number)
        image_urls.append(image_url)
        latitudes.append(latitude)
        longitudes.append(longitude)
        work_times.append(work_time)

        time.sleep(3)

    driver.close()

    time.sleep(3)

    # # 엑셀 파일로 저장하기
    # import openpyxl

    # fpath = r'# 모프 플젝\결과\모프.xlsx'

    # wb = openpyxl.load_workbook(fpath)
    # ws = wb.create_sheet(food) 

    # ws['A1'] = '이름'
    # ws['B1'] = '주소'
    # ws['C1'] = '분류'
    # ws['D1'] = '평점'
    # ws['E1'] = '전화번호'
    # ws['F1'] = '이미지 url'
    # ws['G1'] = '위도'
    # ws['H1'] = '경도'
    # ws['I1'] = '영업시간'


    # for i in range(len(names)):
    #     ws[f'A{i+2}'] = names[i]
    #     ws[f'B{i+2}'] = addresses[i]
    #     ws[f'C{i+2}'] = classifications[i]
    #     ws[f'D{i+2}'] = ranks[i]
    #     ws[f'E{i+2}'] = phone_numbers[i]
    #     ws[f'F{i+2}'] = image_urls[i]
    #     ws[f'G{i+2}'] = latitudes[i]
    #     ws[f'H{i+2}'] = longitudes[i]
    #     ws[f'I{i+2}'] = work_times[i]

    # wb.save(fpath)




