import requests

import config


def get_new_proxies():
    api_response = requests.get(f'https://proxy6.net/api/{config.PROXY_API_KEY}/getproxy').json()
    proxy_list = list(api_response['list'].values())
    return proxy_list


def build_reset_sql(keys):
    sql = 'CREATE TABLE proxies (ROWS);'
    row_str = ''
    for key in keys:
        row_str += f'{key} VARCHAR(90) NOT NULL,'
    sql = sql.replace('ROWS', row_str[:-1])
    return sql


def reset_proxy_table(db, proxy_template):
    cursor = db.cursor()
    if db.table_exists(config.TABLE_PROXIES):
        sql = f'DROP TABLE {config.TABLE_PROXIES}'
        cursor.execute(sql)
        db.commit()
    sql = build_reset_sql(proxy_template.keys())
    cursor.execute(sql)
    db.commit()


def update_proxies(db, proxy_list):
    for proxy in proxy_list:
        db.set_record(config.TABLE_PROXIES, proxy)
        print(proxy)
    db.commit()
