import argparse
import json
import base64
from kafka import KafkaProducer
from config import KafkaConfig


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='从 JSONL 文件导入消息到 Kafka Topic')
    parser.add_argument(
        '-b', '--bootstrap-servers',
        type=str,
        help=f'Kafka broker 地址 (默认: {KafkaConfig().bootstrap_servers})'
    )
    parser.add_argument(
        '-t', '--topic',
        type=str,
        required=True,
        help='Topic 名称 (必填)'
    )
    parser.add_argument(
        '-i', '--input-file',
        type=str,
        help='输入 JSONL 文件路径 (默认: {topic}.jsonl)'
    )
    parser.add_argument(
        '--client-id',
        type=str,
        help='客户端 ID (默认: importer)'
    )
    parser.add_argument(
        '--acks',
        type=int,
        help='Producer acks 设置 (默认: 1)'
    )
    parser.add_argument(
        '--retries',
        type=int,
        help='重试次数 (默认: 3)'
    )
    return parser.parse_args()

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
    """主函数"""
    args = parse_args()

    # 从命令行参数创建配置
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'importer',
        input_file=args.input_file
    )

    # 如果没有指定输入文件，使用 {topic}.jsonl
    input_file = config.input_file
    if not input_file:
        input_file = f'{config.topic_name}.jsonl'

    producer = KafkaProducer(
        bootstrap_servers=config.bootstrap_servers,
        client_id=config.client_id,
        acks=args.acks if args.acks is not None else config.acks,
        retries=args.retries if args.retries is not None else config.retries
    )

    count = 0
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                msg = deserialize_record(record)

                # 发送消息（不指定 partition，让 Kafka 根据 key 自动路由）
                producer.send(
                    topic=config.topic_name,
                    key=msg['key'],
                    value=msg['value'],
                    headers=msg['headers'],
                    timestamp_ms=msg['timestamp_ms']
                )
                count += 1
                if count % 1000 == 0:
                    print(f"已导入 {count} 条消息...")

        producer.flush()
        print(f"✅ 导入完成！共 {count} 条消息到 topic '{config.topic_name}'")
    finally:
        producer.close()

if __name__ == '__main__':
    main()
