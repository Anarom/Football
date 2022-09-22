import os
import json
import time
from multiprocessing import Queue, Process

import config
import database
from driver import get_driver


def get_url_queue():
    queue = Queue()
    db = database.DataBase()
    pairs = db.get_record(config.TABLE_URLS, columns_to_select=['game_id', 'url'], conditions={'status': 0},
                          all_rows=True)
    for pair in pairs:
        queue.put(pair)
    for _ in range(config.DRIVER_PROCS):
        queue.put('end')
    return queue


def parser_proc(id_queue, results_queue):
    driver = get_driver()
    parsed = 0
    while True:
        pair = id_queue.get()
        if pair == 'end':
            results_queue.put('end')
            break
        driver.get(pair[1])
        print(f'{time.strftime("%H:%M:%S")} : {pair[0]} started')
        result = driver.execute_script('return requirejs.s.contexts._.config')
        results_queue.put((pair[0], result))
        parsed += 1
        print(f'{time.strftime("%H:%M:%S")} : {pair[0]} done')
        if parsed and not parsed % config.DRIVER_REFRESH_RATE:
            driver.quit()
            driver = get_driver()
        else:
            time.sleep(config.DRIVER_DELAY)
    driver.quit()


def writer_proc(queue):
    db = database.DataBase()
    results = []
    threads_done = 0
    parsed = len(os.listdir(config.PATH_PARSED_DATA)) * config.DRIVER_REFRESH_RATE
    while threads_done < config.DRIVER_PROCS:
        item = queue.get()
        if item == 'end':
            threads_done += 1
            continue
        else:
            results.append(item)
        if len(results) == config.DRIVER_REFRESH_RATE:
            parsed += len(results)
            save(db, results, parsed)
            results = []
    if results:
        parsed += len(results)
        save(db, results, parsed)


def save(db, results, parsed):
    sql = f'UPDATE {config.TABLE_URLS} SET status=1 WHERE game_id=%s'
    file_num = parsed // config.DRIVER_REFRESH_RATE
    file_path = os.path.join(config.PATH_PARSED_DATA, f'data_{file_num}.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in results:
            json.dump(result[1], file)
            file.write('\n')
            db.crs.execute(sql, (result[0],))
    db.commit()


if __name__ == '__main__':
    procs = []
    url_queue = get_url_queue()
    results_queue = Queue()
    for x in range(config.DRIVER_PROCS):
        proc = Process(target=parser_proc, args=(url_queue, results_queue))
        procs.append(proc)
    procs.append(Process(target=writer_proc, args=(results_queue,)))
    for proc in procs:
        proc.start()
        time.sleep(0.5)
    for proc in procs:
        proc.join()
