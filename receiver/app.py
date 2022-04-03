
from inspect import trace
from pykafka import KafkaClient
import datetime, json
import connexion, yaml, logging, logging.config, uuid
from connexion import NoContent


def generate_trace_id():
    return uuid.uuid4()

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())
    # membership_event = app_config['eventstore1']['url']
    # pt_event = app_config['eventstore2']['url']
    hostname = app_config['events']['hostname']
    port = app_config['events']['port']
    t = app_config['events']['topic']


with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config) 
    logger = logging.getLogger('basicLogger')

def add_gym_member(body):
    """ Receives a membership event"""

    trace_id = f'{generate_trace_id()}'
    body['trace_id'] = trace_id
    # response = requests.post(membership_event, json=body, headers={"content-type": "application/json"})
    # status_code = response.status_code
    client = KafkaClient(hosts=f'{hostname}:{port}')
    topic = client.topics[str.encode(t)]
    producer = topic.get_sync_producer()
    msg = {"type": "membership",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201
    logger.info(f'Received event membership request with a trace id of {trace_id}')
    logger.info(f'Returned event membership response (Id: {trace_id}) with status {status_code}')
    return NoContent, 201


def book_pt_session(body):
    """ Receives a pt session event """

    trace_id = f'{generate_trace_id()}'
    body['trace_id'] = trace_id
    # response = requests.post(pt_event, json=body, headers={"content-type": "application/json"})
    # status_code = response.status_code
    client = KafkaClient(hosts=f'{hostname}:{port}')
    topic = client.topics[str.encode(t)]
    producer = topic.get_sync_producer()
    msg = {"type": "pt",
           "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201
    logger.info(f'Received event pt-session request with a trace id of {trace_id}')
    logger.info(f'Returned event pt-session response (Id: {trace_id}) with status {status_code}')
    
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)