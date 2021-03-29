import configparser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from Logger import get_log
import datetime
import spider_main

# 读取配置文件
config = configparser.RawConfigParser()
config.read("./temp/cfg.ini")
logger = get_log()


def Start():
    List = config.get("urls", "List").split('\n')
    for url in List:
        spider_main.Start(url)


def my_listener(event):
    if event.exception:
        logger.debug("*********************************Crawller got a ERROR: "+str(event.exception)+" ********")
        print("Something went wrong...")
    else:
        logger.debug("*****************************"
                     "****Crawller KEEP running...*********************************")
        print("Running as usual...")


if __name__ == "__main__":
    print("Awaiting...")
    # scheduler = BlockingScheduler()
    # scheduler.add_job(func=Start, trigger='cron', hour="8,10,14,17,19,21,23", id='date_task')
    # scheduler.add_job(func=Start, trigger='cron', hour=20, minute=15, second=30, id='date_task')
    # scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    # scheduler._logger = logger
    # scheduler.start()
    Start()
