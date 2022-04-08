
from inspect import trace
import requests
from pykafka import KafkaClient
import datetime, json
import connexion, yaml, logging, logging.config, uuid
from connexion import NoContent
from flask_cors import CORS, cross_origin

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())
    host = app_config['events']['hostname']
    port = app_config['events']['port']
    t = app_config['events']['topic']


with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
    logger = logging.getLogger('basicLogger')

def get_gym_member(index):
    """ Get gym membership in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving gym membership at index %d" % index)
    i = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info(f"the msg is {msg}")
            if msg["type"] == "membership":
                if i == index:
                    return msg["payload"], 200
                else:
                    i = i + 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find gym membership at index %d" % index)
    return {"message": "Not Found"}, 404

def get_pt_session(index):
    """ Get pt session in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    logger.info("Retrieving pt session at index %d" % index)
    i = 0
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            logger.info(f"the msg is {msg}")
            if msg["type"] == "pt":
                if i == index:
                    return msg["payload"], 200
                else:
                    i = i + 1
    except:
        logger.error("No more messages found")
    logger.error("Could not find gym membership at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(port=8110)
