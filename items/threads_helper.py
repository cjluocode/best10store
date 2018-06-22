from multiprocessing.dummy import Pool as ThreadPool

import datetime


class MultiThreadsClass(object):
    def run_multi(self, activate_func, all_yield, thread_count=14, caption='Start threads'):

        start_time = datetime.datetime.utcnow()
        print("___Starting up to {} threads at {}___".format(thread_count,start_time.isoformat()))  # Or use caption

        pool = ThreadPool(thread_count)
        self.results = pool.map(activate_func, all_yield)
        pool.close()
        pool.join()

        end_time = datetime.datetime.utcnow()
        print("___Finished up to {} threads at {}___".format(thread_count,end_time.isoformat()))  # Or use caption
        print("(Elapsed time: {} secs)".format((end_time - start_time).seconds))
