

import json
from multiprocessing import Process, Value, Array, Pool
import multiprocessing
import access as grab


input_file = json.loads(open('penny_stocks.json').read())

                         
portfolio = input_file

def processing_fn(datapoints):
    securities_ipo = {}
    for value in portfolio:
        try:
            dummy_ = grab.grab(str(value), datapoints)
            securities_ipo[str(value)] = str(dummy_.data.index[0])
        except Exception as e:
            print("There was an issue processing symbol %s with error %s" % (dummy_.data.stock, e))
            return
            
        with open('pennystocks_ipo.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(securities_ipo, ensure_ascii=False))

if __name__ == '__main__':
    cpu_cores = multiprocessing.cpu_count()
    with Pool(processes = cpu_cores) as pool:
        result = pool.map(processing_fn(25000), portfolio, 5)
