import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

DLT_BASE_URL = 'https://cp.china-ssq.net/dlt/info/'
def dlt_crawler(issue='07001'):
    response = requests.get(f'{DLT_BASE_URL}{issue}')
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    
    # Initialize the main dictionary to store all information
    data = {}

    # Extract basic info like draw number, date, and sales information
    info_section = soup.find('div', class_='kj-information')
    draw_number = info_section.find('div', class_='issue-num').text.strip().replace('第\xa0','').replace('\xa0期','')
    if draw_number != issue:
        return None
    # Extract draw details
    data['Lottery Name'] = info_section.find('div', class_='tit').text.strip()
    data['Draw Number'] = draw_number
    data['Draw Date'] = info_section.find('div', class_='kj-data').text.strip().replace('开奖日期：','开奖日期：')
    data['Draw Time'] = info_section.find('div', class_='kj-time').text.strip()

    # Extract winning numbers
    winning_numbers_section = info_section.find('div', class_='kj-ball')
    red_balls = [em.text.strip() for em in winning_numbers_section.find_all('em')[:-2]]  # Red balls
    blue_balls = [em.text.strip() for em in winning_numbers_section.find_all('em')[-2:]]  # Blue balls
    data['Winning Numbers'] = {
        'Red Balls': red_balls,
        'Blue Balls': blue_balls
    }

    # Extract sales volume and prize pool
    sales_info = info_section.find_all('div', class_='sales-volume')
    data['Sales Volume'] = sales_info[0].find('span', class_='c-red').text.strip()
    data['Prize Pool'] = sales_info[1].find('span', class_='c-red').text.strip()

    # Extract the table data (main prize details and additional prize details)
    tables = soup.find_all('table')

    # List to hold table information
    table_data = []

    # Process each table
    for table in tables:
        headers = [td.text.strip() for td in table.find_all('td')[:4]]  # Extract table headers
        table_rows = []
        
        # Extract rows
        for row in table.find_all('tr')[1:]:  # Skip header row
            columns = [td.text.strip() for td in row.find_all('td')]
            row_dict = dict(zip(headers, columns))
            table_rows.append(row_dict)
        
        # Append the table's data to the list
        table_data.append(table_rows)

    # Add table data to the main dictionary
    data['Prize Breakdown'] = table_data[0]  # First table (main prize data)
    data['Additional Prize Breakdown'] = table_data[1]  # Second table (additional prize data)

    # Output the complete dictionary
    return data

def dlt_dictlist2pandas(data_list):
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
            'Blue Balls': ','.join(data['Winning Numbers']['Blue Balls']),  # 将蓝球数据合并为字符串
            'Sales Volume': data['Sales Volume'],
            'Prize Pool': data['Prize Pool']
        }
        
        # 将奖项明细分为单独的列（每条记录只保留一等奖和二等奖信息）
        for prize in data['Prize Breakdown']:
            prize_name = prize['奖项']
            record[f'{prize_name} 中奖条件'] = prize['中奖条件']
            record[f'{prize_name} 中奖注数'] = prize['中奖注数']
            record[f'{prize_name} 每注奖金(元)'] = prize['每注奖金(元)']
        
        # 同理，处理追加奖项
        for prize in data['Additional Prize Breakdown']:
            prize_name = prize['奖项']
            record[f'{prize_name} 中奖注数'] = prize['中奖注数']
            record[f'{prize_name} 每注奖金(元)'] = prize['每注奖金(元)']
        
        # 将当前记录添加到 records 列表中
        records.append(record)
    # 将 records 列表转换为 DataFrame
    df = pd.DataFrame(records)
    return df

def get_all_dlt_data_by_year(year='07', from_issue=1):
    data_list = []
    from_issue = from_issue
    progress = tqdm()
    progress.set_postfix_str(f'Year: {year}')
    while True:
        issue = f'{year}{from_issue:03d}'
        data = dlt_crawler(issue=issue)
        if data is None:
            print(f'\nWarning: Draw number mismatch! Expected: {issue}')
            break
        data_list.append(data)
        from_issue += 1
        progress.set_description(f'Processed: {issue} downloaded!')
    return data_list

def save_dlt_data(rootdir='./data',year='07'):
    if (not os.path.exists(rootdir)):
        os.mkdir(rootdir)
    data_list = get_all_dlt_data_by_year(year=year)
    pd_data = dlt_dictlist2pandas(data_list)
    pd_data.to_csv(os.path.join(rootdir,f'dlt_{year}.csv'), index=False)

def add_dlt_data(rootdir='./data',year='07'):
    csv_file = os.path.join(rootdir,f'dlt_{year}.csv')
    if os.path.exists(csv_file):
        # Read the existing CSV file
        existing_data = pd.read_csv(csv_file)
        # Find the last 'Draw Number' in the file
        last_draw_number = existing_data['Draw Number'].values[-1]
        dn = int(str(last_draw_number)[-3:])
        print(f'Last draw number: {dn}')
        data_list = get_all_dlt_data_by_year(year=year,from_issue=dn+1)
        new_data = dlt_dictlist2pandas(data_list)
        # Append the new data to the existing data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(csv_file, index=False)
    else:
        print(f'File not found: {csv_file}')
        save_dlt_data(rootdir=rootdir,year=year)

if __name__=='__main__':
    save_dlt_data(year='07')
    # add_dlt_data(year='07')