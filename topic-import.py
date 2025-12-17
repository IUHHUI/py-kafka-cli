import json
import base64
from kafka import KafkaProducer

TEST_BOOTSTRAP = 'localhost:9092'  # 改为你的测试 Kafka 地址
TOPIC = 'prod.hkex.news.ndsdata'   
INPUT_FILE = f'{TOPIC}.jsonl'

def deserialize_record(record):
    """从 JSON 记录还原为原始字段"""
    key = base64.b64decode(record['key']) if record['key'] else None
    value = base64.b64decode(record['value']) if record['value'] else None
    headers = [(k, base64.b64decode(v)) for k, v in record['headers']] if record['headers'] else None
    return {
        'key': key,
        'value': value,
        'headers': headers,
        'timestamp_ms': record['timestamp'] if record['timestamp'] > 0 else None
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers=TEST_BOOTSTRAP,
        client_id='importer',
        acks=1,
        retries=3
    )

    count = 0
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            msg = deserialize_record(record)

            # 发送消息（不指定 partition，让 Kafka 根据 key 自动路由）
            producer.send(
                topic=TOPIC,
                key=msg['key'],
                value=msg['value'],
                headers=msg['headers'],
                timestamp_ms=msg['timestamp_ms']
            )
            count += 1
            if count % 1000 == 0:
                print(f"已导入 {count} 条消息...")

    producer.flush()
    producer.close()
    print(f"✅ 导入完成！共 {count} 条消息到 topic '{TOPIC}'")

if __name__ == '__main__':
    main()
