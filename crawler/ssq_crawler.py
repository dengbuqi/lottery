import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

SSQ_BASE_URL = 'https://cp.china-ssq.net/ssq/info/'

def ssq_crawler(issue='2003001'):
    response = requests.get(f'{SSQ_BASE_URL}{issue}')
    html_content = response.text

    # 解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 初始化主字典以存储所有信息
    data = {}

    # 提取基本信息，如开奖期号、日期、销售额信息
    info_section = soup.find('div', class_='kj-information')
    draw_number = info_section.find('div', class_='issue-num').text.strip().replace('第\xa0','').replace('\xa0期','')
    if draw_number != issue:
        return None
    
    # 提取开奖详细信息
    data['Lottery Name'] = info_section.find('div', class_='tit').text.strip()
    data['Draw Number'] = draw_number
    data['Draw Date'] = info_section.find('div', class_='kj-data').text.strip().replace('开奖日期：','开奖日期：')
    data['Draw Time'] = info_section.find('div', class_='kj-time').text.strip()

    # 提取中奖号码
    winning_numbers_section = info_section.find('div', class_='kj-ball')
    red_balls = [em.text.strip() for em in winning_numbers_section.find_all('em')[:-1]]  # 红球
    blue_ball = [em.text.strip() for em in winning_numbers_section.find_all('em')[-1]]  # 蓝球
    data['Winning Numbers'] = {
        'Red Balls': red_balls,
        'Blue Ball': blue_ball[0]
    }

    # 提取销售额和奖池
    sales_info = info_section.find_all('div', class_='sales-volume')
    data['Sales Volume'] = sales_info[0].find('span', class_='c-red').text.strip()
    data['Prize Pool'] = sales_info[1].find('span', class_='c-red').text.strip()

    # 提取表格数据（奖项详情）
    tables = soup.find_all('table')

    # 存储表格信息的列表
    table_data = []

    # 处理每个表格
    for table in tables:
        headers = [td.text.strip() for td in table.find_all('td')[:4]]  # 提取表头
        table_rows = []
        
        # 提取表格行
        for row in table.find_all('tr')[1:]:  # 跳过表头行
            columns = [td.text.strip() for td in row.find_all('td')]
            row_dict = dict(zip(headers, columns))
            table_rows.append(row_dict)
        
        # 将表格的数据附加到列表中
        table_data.append(table_rows)

    # 将表格数据添加到主字典
    data['Prize Breakdown'] = table_data[0]  # 第一个表格（主要奖项数据）

    # 输出完整的字典
    return data

def ssq_dictlist2pandas(data_list):
    records = []

    # 遍历每一个 data 字典
    for data in data_list:
        # 基本信息
        record = {
            'Lottery Name': data['Lottery Name'],
            'Draw Number': data['Draw Number'],
            'Draw Date': data['Draw Date'],
            'Draw Time': data['Draw Time'],
            'Red Balls': ','.join(data['Winning Numbers']['Red Balls']),  # 将红球数据合并为字符串
            'Blue Ball': data['Winning Numbers']['Blue Ball'],  # 蓝球数据
            'Sales Volume': data['Sales Volume'],
            'Prize Pool': data['Prize Pool']
        }
        
        # 将奖项明细分为单独的列（每条记录只保留奖项信息）
        for prize in data['Prize Breakdown']:
            prize_name = prize['奖项']
            record[f'{prize_name} 中奖条件'] = prize['中奖条件']
            record[f'{prize_name} 中奖注数'] = prize['中奖注数']
            record[f'{prize_name} 每注奖金(元)'] = prize['每注奖金(元)']
        
        # 将当前记录添加到 records 列表中
        records.append(record)
    # 将 records 列表转换为 DataFrame
    df = pd.DataFrame(records)
    return df

def get_all_ssq_data_by_year(year='2003',from_issue=1):
    data_list = []
    i = from_issue
    progress = tqdm()
    progress.set_postfix_str(f'Year: {year}')
    while True:
        issue = f'{year}{i:03d}'
        data = ssq_crawler(issue=issue)
        if data is None:
            print(f'\nWarning: Draw number mismatch! Expected: {issue}')
            break
        data_list.append(data)
        i += 1
        progress.set_description(f'Processed: {issue} downloaded!')
    return data_list

def save_ssq_data(rootdir='./data',year='2003'):
    data_list = get_all_ssq_data_by_year(year=year)
    pd_data = ssq_dictlist2pandas(data_list)
    pd_data.to_csv(os.path.join(rootdir,f'ssq_{year}.csv'), index=False)

def add_ssq_data(rootdir='./data',year='2003'):
    csv_file = os.path.join(rootdir,f'ssq_{year}.csv')
    if os.path.exists(csv_file):
        # Read the existing CSV file
        existing_data = pd.read_csv(csv_file)
        # Find the last 'Draw Number' in the file
        last_draw_number = existing_data['Draw Number'].values[-1]
        dn = int(str(last_draw_number)[-3:])
        print(f'Last draw number: {dn}')
        data_list = get_all_ssq_data_by_year(year=year,from_issue=dn+1)
        new_data = ssq_dictlist2pandas(data_list)
        # Append the new data to the existing data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(csv_file, index=False)
    else:
        print(f'File not found: {csv_file}')
        save_ssq_data(rootdir=rootdir,year=year)

if __name__=='__main__':
    # save_ssq_data(year='2003')
    add_ssq_data(year='2003')