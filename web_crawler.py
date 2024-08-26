from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

csv_column = ['教師', '作者', '論文名稱', '會議名稱', '地點']

def read_txt(path):
    content = []
    with open(path) as f:
        for line in f.readlines():
            content.append(line.strip())
    return content

def web_crawler(professor_list, save_path):
    driver = webdriver.Chrome()
    with open(save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_column)

        for i, professor in enumerate(professor_list):
            if i == 0:
                driver.get("https://researchoutput.ncku.edu.tw/zh/")
                search = driver.find_element(By.ID, 'global-search-input')
            else:
                search = driver.find_element(By.ID, 'main-search')

            search.send_keys(professor)
            search.send_keys(Keys.ENTER)
            # time.sleep(2)

            results = driver.find_element(By.XPATH, '//a[contains(@href, "https://researchoutput.ncku.edu.tw/zh/persons/")]')
            results.click()
            time.sleep(2)

            research_page = driver.find_elements(By.XPATH, '//span[contains(@class, "label") and contains(text(), "研究成果")]')
            research_page[0].click()
            time.sleep(2)

            Conference_page = driver.find_elements(By.XPATH, '//a[contains(@class, "portal_link count increment-counter") and contains(@aria-label, "Conference contribution")]')
            if len(Conference_page) == 0:
                continue
            else:
                Conference_page[0].click()
                time.sleep(2)
            
            ### get 2023 conference index ###
            idx_list = []
            Conferences = driver.find_elements(By.CSS_SELECTOR, '.list-result-item')
            for i, item in enumerate(Conferences):

                conference_info = item.text.split('\n')
                if conference_info[0] == '2023':
                    class_name = item.get_attribute('class').strip().split('-')[-1]
                    idx_list.append(int(class_name))
                elif conference_info[0].isdigit() and int(conference_info[0]) < 2023:
                    break
                elif conference_info[0].isdigit() and int(conference_info[0]) > 2023:
                    continue
                else:
                    class_name = item.get_attribute('class').strip().split('-')[-1]
                    idx_list.append(int(class_name))
            
            print('\n')
            print(professor, idx_list)
            for idx in idx_list:
                write_row = []
                Conferences = driver.find_elements(By.XPATH, '//h3[contains(@class, "title")]')
                Conferences[idx].click()
                time.sleep(3)

                # event_info = driver.find_element(By.XPATH, '//tr[contains(@class, "event")]').find_element(By.XPATH, '//span[contains(@class, "prefix")]').text.strip()
                title = driver.find_element(By.CSS_SELECTOR, 'div.rendering h1 span').text.strip()
                author = driver.find_element(By.XPATH, '//p[contains(@class, "relations persons")]').text.strip()
                # event_info = driver.find_element(By.CSS_SELECTOR, 'tr.event').find_element(By.CSS_SELECTOR, 'td').text.split('\n')
                event_name = driver.find_element(By.XPATH, '//tr[./th[contains(text(), "Conference")]]/td').text.strip()
                event_loc = driver.find_elements(By.XPATH, '//tr[./th[contains(text(), "國家/地區")]]/td')
                if len(event_loc) != 0:
                    event_loc = event_loc[0].text.strip()
                else:
                    event_loc = 'None'

                write_row.append(professor)
                write_row.append(author)
                write_row.append(title)
                write_row.append(event_name)
                write_row.append(event_loc)

                # print('professor :', professor)
                print('author :', author)
                print('title :', title)
                print('event :', event_name)
                print('location :', event_loc)

                driver.back()
                print('------------------------------------')
                writer.writerow(write_row)
            

    # time.sleep(100)
    driver.close() # 關閉瀏覽器視窗

if __name__ == '__main__':
    path = 'professor_2.txt'
    save_path = 'output_2.csv'
    professor_list = read_txt(path)
    # print(professor_list)
    # web_crawler(['謝孫源'])
    web_crawler(professor_list, save_path)