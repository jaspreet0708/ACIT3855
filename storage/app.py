import connexion, yaml, logging, logging.config
from connexion import NoContent
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from base import Base
from add_gym_member import GymMember
from book_pt_session import PTSession
import datetime, json, time

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    user = app_config['datastore']['user']
    password = app_config['datastore']['password']
    host = app_config['datastore']['hostname']
    port = app_config['datastore']['port']
    db = app_config['datastore']['db']
    retries = app_config['events']['retry']
    go_sleepy = app_config['events']['sleep']

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info(f"Connecting to DB Hostname: {host}, Port: {port}")


def get_gym_member(start_timestamp, end_timestamp): 
    """ Gets new blood pressure readings after the timestamp """ 
 
    session = DB_SESSION() 
 
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ") 
    print(f"loading entires from {start_timestamp_datetime} to {end_timestamp_datetime}")
 
    readings = session.query(GymMember).filter(and_(GymMember.date_created >= start_timestamp_datetime, GymMember.date_created < end_timestamp_datetime)) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info(f"Query for membership requests for {start_timestamp_datetime} to {end_timestamp_datetime} returns {len(results_list)} results") 
 
    return results_list, 200


def get_pt_session(start_timestamp, end_timestamp): 
    """ Gets new blood pressure readings after the timestamp """ 
 
    session = DB_SESSION() 
 
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ") 
    print(f"loading entires from {start_timestamp_datetime} to {end_timestamp_datetime}")

    readings = session.query(PTSession).filter(and_(PTSession.date_created >= start_timestamp_datetime, PTSession.date_created < end_timestamp_datetime)) 
 
    results_list = [] 
 
    for reading in readings: 
        results_list.append(reading.to_dict()) 
 
    session.close() 
     
    logger.info(f"Query for pt-session requests for {start_timestamp_datetime} to {end_timestamp_datetime} returns {len(results_list)} results") 
 
    return results_list, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    retry = 0
    while(retry<=retries):
        logger.info(f'Trying to connect to kafka producer, retrying kafak consumer....TRY {retry}')
        try:
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
        except:
            print(f'THERE IS error connecting to kafka')
            pass
        time.sleep(go_sleepy)
        retry = retry + 1

        
    consumer = topic.get_simple_consumer(consumer_group=b'bruh_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)


    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "membership":
            session = DB_SESSION()
            gm = GymMember(
                payload['user_info']['user_id'],
                payload['user_info']['user_name'],
                payload['user_info']['user_weight'],
                payload['user_info']['user_height'],
                payload['user_info']['user_address'],
                payload['gym_address'],
                payload['membership_months'],
                payload['start_date'],
                payload['timestamp'],
                payload['trace_id']
            )
            session.add(gm)
            session.commit()
            logger.debug(f"Stored event membership request with a trace id of {payload['trace_id']}")
            logger.info("Added payload to membership event ")
            session.close()

        elif msg["type"] == "pt":
            session = DB_SESSION()
            pt = PTSession(
                payload['user_info']['user_id'],
                payload['user_info']['user_name'],
                payload['user_info']['user_weight'],
                payload['user_info']['user_height'],
                payload['user_info']['user_address'],
                payload['trainer_id'],
                payload['duration_hours'],
                payload['start_time'],
                payload['timestamp'],
                payload['trace_id']
            )
            session.add(pt)
            session.commit()
            logger.debug(f"Stored event pt-session request with a trace id of {payload['trace_id']}")
            logger.info("Added payload to pt event ")
            session.close()

        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(host='0.0.0.0' ,port=8090)

