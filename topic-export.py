import argparse
import json
import base64
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from config import KafkaConfig


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='从 Kafka Topic 导出消息到 JSONL 文件')
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
        '-o', '--output-file',
        type=str,
        help='输出 JSONL 文件路径 (默认: {topic}.jsonl)'
    )
    parser.add_argument(
        '--client-id',
        type=str,
        help='客户端 ID (默认: exporter)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        help='Consumer 超时时间（毫秒），默认 20000'
    )
    return parser.parse_args()

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
    """主函数"""
    args = parse_args()

    # 从命令行参数创建配置
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'exporter',
        output_file=args.output_file,
        timeout_ms=args.timeout
    )

    # 如果没有指定输出文件，使用 {topic}.jsonl
    output_file = config.output_file
    if not output_file:
        output_file = f'{config.topic_name}.jsonl'

    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
        auto_offset_reset='earliest',  # 从头开始
        enable_auto_commit=False,
        consumer_timeout_ms=config.timeout_ms,
        client_id=config.client_id
    )

    try:
        # 获取所有分区
        partitions = consumer.partitions_for_topic(config.topic_name)
        if not partitions:
            raise RuntimeError(f"Topic {config.topic_name} not found")

        # 分配所有分区
        consumer.assign([TopicPartition(config.topic_name, p) for p in partitions])
        print(f"开始导出 topic '{config.topic_name}' 共 {len(partitions)} 个分区...")

        count = 0
        with open(output_file, 'w', encoding='utf-8') as f:
            for msg in consumer:
                record = serialize_message(msg)
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
                count += 1
                if count % 1000 == 0:
                    print(f"已导出 {count} 条消息...")

        print(f"✅ 导出完成！共 {count} 条消息，保存到 {output_file}")
    finally:
        consumer.close()

if __name__ == '__main__':
    main()
