import requests
from bs4 import BeautifulSoup

# 設定
page_from = 1
page_to = 20

def main():
    # 外面列表
    url = 'https://www.tmbia.org.tw/member.php?&page=4'
    # print(getDetailUrlListFromUrl(url))
    page_urls = ['https://www.tmbia.org.tw/member.php?&page='+str(x) for x in range(page_from, page_to+1)]
    seed_urls = []

    # 分析出所有要拜訪的頁面 url
    print('正在生成所有公司網址，請稍後...')
    for page_url in page_urls:
        seed_urls = seed_urls + getDetailUrlListFromUrl(page_url)

    # 裡面詳細
    for seed_url in seed_urls:
        print(getCompInfoFromUrl(seed_url))


def getDetailUrlListFromUrl(url):
    # url 範例：https://www.tmbia.org.tw/member.php?&page=4
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    ret = []

    links = soup.select('.member_Name_Btn')
    for node_link in links:
        ret.append('https://www.tmbia.org.tw/' + node_link.get('href'))
    return ret

def getCompInfoFromUrl(url):
    # url 範例：https://www.tmbia.org.tw/member_detail.php?id=1
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    ret = ''

    try:
        # 公司名稱
        comp_name = soup.select('.member_Table_Td')[3].getText()

        # 統一編號
        comp_number = soup.select('.member_Table_Td')[1].getText()

        # 負責人
        comp_principle = soup.select('.member_Table_Td')[2].getText()

        # 公司地址
        comp_address = soup.select('.member_Table_Td')[4].getText()

        # 公司電話
        comp_tel = soup.select('.member_Table_Td')[5].getText()
        
        # 公司傳真
        comp_fax = soup.select('.member_Table_Td')[6].getText()
        
        # email
        comp_email = soup.select('.member_Table_Td')[7].getText()
        
        # 公司網址
        comp_website = soup.select('.member_Table_Td')[8].getText()
        
        # 工廠地址
        fact_address = soup.select('.member_Table_Td')[9].getText()
        
        # 工廠電話
        fact_tel = soup.select('.member_Table_Td')[10].getText()

        # 工廠傳真
        fact_fax = soup.select('.member_Table_Td')[11].getText()

        # 營業項目
        comp_project = cleanText(str(soup.select('.member_Table_Td')[12]))
        
        # 輸出格式
        ret = '{0}${1}${2}${3}${4}${5}${6}${7}${8}${9}${10}${11}'.format(comp_name, comp_number, comp_principle, comp_address, comp_tel, comp_fax, comp_email, comp_website, fact_address, fact_tel, fact_fax, comp_project)
        
    except:
        ret = ''

    return ret

def cleanText(originText):
    ''' 移除不必要的換行 '''
    ret = originText
    ret = ret.replace('<td class="member_Table_Td">', '')
    ret = ret.replace('</td>', '')
    ret = ret.replace('<br/>', '')
    ret = ret.replace('\r', '')
    ret = ret.replace('\n', '')
    return ret

main()
