import pickle
import time
#from sqlalchemy import create_engine
import tushare as ts
import get_date as gd
import argparse
import concurrent.futures
import multiprocessing
import Qtrac

def get_ticks():
    t0 = time.perf_counter()
    concurrency, Sdate, Edate = handle_commandline()
    codefile = 'codes'
    Qtrac.report("starting...")
    futures = set()
    dates = gd.get_date(Sdate, Edate)
    codes = []
    datas = []
    with open(codefile) as cf:
        for each in cf:
            codes.append(each.strip())
    for a in codes:
        for b in dates:
            datas.append([a,b])
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=concurrency) as executor:
        for data in datas:
            future = executor.submit(get_tick, data)
            futures.add(future)
        done, canceled = process(futures)
        if canceled:
            executor.shutdown()
    Qtrac.report("read {}/{} tickdata using {} threads{}".format(done,
        len(futures),concurrency, "[canceled]" if canceled else ""))
    print()
    t1 = time.perf_counter()
    print(t1-t0)
    if not canceled:
        print('not canceled')

def process(futures):
    canceled = False
    done = 0
    pickledata = []
    #engine = create_engine('mysql://root:770607@127.0.0.1/tickdata?charset=utf8')
    canceled, results = wait_for(futures)
    if not canceled:
        for result in(result for ok,result in results if ok and 
                result is not None):
            done +=1
            #result[2].to_sql(result[0]+'t'+result[1], engine)
            pickledata.append(result)
        with open('/Volumes/ST HDD/stock/tick/'+pickledata[0][1][:7]+'.txt', 'wb') as rfile:
            pickle.dump(pickledata, rfile, pickle.HIGHEST_PROTOCOL)
    else:
        done = sum(1 for ok, result in results if ok and result is not None)
    return done, canceled

def wait_for(futures):
    canceled = False
    results = []
    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is None:
                ok, result = future.result()
                if not ok:
                    Qtrac.report(result, True)
                elif result is not None:
                    Qtrac.report("read {}".format(result[2]['time'][0:5]))
                results.append((ok, result))
            else:
                raise err
    except KeyboardInterrupt:
        Qtrac.report('canceling...')
        canceled = True
        for future in futures:
            future.cancel()
    return canceled, results

def get_tick(s):
    try:
        df = ts.get_tick_data(s[0], s[1], retry_count=20)
        try:
            df['time'][5]
        except KeyError:
            return True, None
        return True, [s[0], s[1], df]
    except IndexError as err:
        return False, "Error: {}: {}".format(s[0]+s[1], err)

def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--concurrency", type=int,
            default=multiprocessing.cpu_count()*4,
            help="specify the concurrency (for debugging and "
            "timing) [default: %(default)d]")
    parser.add_argument("-s", "--startdate", type=str,
            default='2016-12-28')
    parser.add_argument("-e", "--enddate", type=str,
            default='2016-12-29')
    args = parser.parse_args()
    return args.concurrency, args.startdate, args.enddate

if __name__ == '__main__':
    get_ticks()
