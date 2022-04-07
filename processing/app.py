
from inspect import trace
# from xxlimited import new
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import connexion, yaml, logging, logging.config, uuid
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stats import Stats
from base import Base
import datetime


with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())
    pull = app_config["datastore"]["filename"]


with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'sqlite:///{pull}') 
Base.metadata.bind = DB_ENGINE 
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def populate_stats(): 
    """ Periodically update stats """ 
    logger.info('Start Periodic Processing')
    result = {'num_membership': 1, 'num_pt_session': 1, 'max_height': 1, 'max_weight': 1, 'last_updated': '1'} # default stats
    session = DB_SESSION() 
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    result = results[0]
    session.close() 
    last_update_timestamp =result.last_updated.strftime("%Y-%m-%dT%H:%M:%SZ") 
    
    current = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    response1 = requests.get(f"{app_config['eventstore']['url']}/membership", params= {'timestamp': last_update_timestamp})
    response2 = requests.get(f"{app_config['eventstore']['url']}/pt-session", params= {'timestamp': last_update_timestamp})
    if(response1.status_code !=200):
        logger.error('membership get event did not return 200 code')
    if(response2.status_code != 200):
        logger.error('pt-session get event did not return 200 code')
    data1 = response1.json()
    data2 = response2.json()
    logger.info(f'number of membership events received: {len(data1)}') 
    logger.info(f'number of pt-session events received: {len(data2)}')
    new_stats = {'num_membership': result.num_membership, 'num_pt_session': result.num_pt_session, 'max_height': result.max_height, 'max_weight': result.max_weight, 'last_updated': current}  
    for i in data1:
        t = i['trace_id']
        logger.debug(f'membership event with trace id {t} is processed')
        height = i['user_info']['user_height']
        weight = i['user_info']['user_weight']
        if (height > result.max_height):
            new_stats['max_height'] = height
        
        if (weight > result.max_weight):
            new_stats['max_weight'] = weight
        

    for i in data2:
        t = i['trace_id']
        logger.debug(f'pt-session event with trace id {t} is processed')
        height = i['user_info']['user_height']
        weight = i['user_info']['user_weight']
        if (height > result.max_height):
            new_stats['max_height'] = height
        
        if (weight > result.max_weight):
            new_stats['max_weight'] = weight

    new_stats['num_membership'] = new_stats['num_membership'] + len(data1) 
    new_stats['num_pt_session'] = new_stats['num_pt_session'] + len(data2) 
    new_stats['last_updated'] = current
    print(new_stats)
    session = DB_SESSION() 
 
    commit_stats = Stats(new_stats['num_membership'], 
                new_stats['num_pt_session'], 
                new_stats['max_height'], 
                new_stats['max_weight'], 
                datetime.datetime.strptime(new_stats['last_updated'],"%Y-%m-%dT%H:%M:%SZ"))
    
    session.add(commit_stats) 
    
    session.commit() 
    logger.debug(f'latest stats object entered is: {new_stats}')
    session.close() 
    logger.info('Finished periodic processing')
    

    

def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec']) 
    sched.start()

def get_stats(): 
    """ Gets processed stats from sqlite database """ 
    logger.info('Start get request for stats')
    result = {'num_membership': 1, 'num_pt_session': 1, 'max_height': 1, 'max_weight': 1, 'last_updated': '1'} # default stats

    session = DB_SESSION() 
    results = session.query(Stats).order_by(Stats.last_updated.desc())
    result = results[0]
    session.close()
    
    stats = {'num_membership': result.num_membership, 'num_pt_session': result.num_pt_session, 'max_height': result.max_height, 'max_weight': result.max_weight, 'last_updated': result.last_updated}

    logger.debug(f'latest stats object that has been returned is : {stats}')
    logger.info('Finished get request')

    return stats, 200

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__": 
    # run our standalone gevent server 
    init_scheduler() 
    app.run(port=8100, use_reloader=False)