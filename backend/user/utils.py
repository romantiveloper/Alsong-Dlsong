from datetime import datetime

def parse_birthday(input_date):
    
    # 입력값이 None이라면, None을 반환하고 함수 종료
    if input_date is None:
        return None
        
    formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y%m%d', '%m-%d', '%m/%d', '%m.%d', '%m%d']

    for date_format in formats:
        try:
            parsed_date = datetime.strptime(input_date, date_format).date()
            
            if len(str(input_date)) == 4:
                date_format = "0000" + date_format
            
            return parsed_date
            
        except ValueError:
            continue

    raise ValueError(f"{input_date}는 날짜 형식이 맞지 않습니다. 'YYYY-MM-DD', 'YYYY/MM/DD', 'YYYY.MM.DD', 'YYYYMMDD', 'MM-DD', 'MM/DD', 'MM.DD', 'MMDD' 형식 중 하나여야 합니다.")
