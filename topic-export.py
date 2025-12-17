import json
import base64
from kafka import KafkaConsumer
from kafka.structs import TopicPartition

BOOTSTRAP_SERVERS = '192.168.220.220:9092'
TOPIC = 'prod.hkex.news.ndsdata'
OUTPUT_FILE = f'{TOPIC}.jsonl'

def serialize_message(msg):
    """将 Kafka 消息转为可 JSON 序列化的字典"""
    return {
        'partition': msg.partition,
        'offset': msg.offset,
        'key': base64.b64encode(msg.key).decode('utf-8') if msg.key else None,
        'value': base64.b64encode(msg.value).decode('utf-8') if msg.value else None,
        'headers': [(k, base64.b64encode(v).decode('utf-8')) for k, v in msg.headers] if msg.headers else [],
        'timestamp': msg.timestamp
    }

def main():
    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',  # 从头开始
        enable_auto_commit=False,
        consumer_timeout_ms=20000,     # 20s 无消息退出
        client_id='exporter'
    )

    # 获取所有分区
    partitions = consumer.partitions_for_topic(TOPIC)
    if not partitions:
        raise RuntimeError(f"Topic {TOPIC} not found")

    # 分配所有分区
    consumer.assign([TopicPartition(TOPIC, p) for p in partitions])
    print(f"开始导出 topic '{TOPIC}' 共 {len(partitions)} 个分区...")

    count = 0
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for msg in consumer:
            record = serialize_message(msg)
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
            count += 1
            if count % 1000 == 0:
                print(f"已导出 {count} 条消息...")

    print(f"✅ 导出完成！共 {count} 条消息，保存到 {OUTPUT_FILE}")
    consumer.close()

if __name__ == '__main__':
    main()
