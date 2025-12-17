#!/usr/bin/env python
"""
Kafka CLI - 统一的 Kafka 命令行工具
"""
import argparse
import sys
import json
import base64
from kafka.admin import KafkaAdminClient
from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition
from config import KafkaConfig


def cmd_list(args):
    """列出所有 Topics"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        client_id=args.client_id or 'kafka-cli-list'
    )

    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers,
            client_id=config.client_id
        )

        topic_list = admin_client.list_topics()

        print("Kafka 集群中的 Topics:")
        for topic in sorted(topic_list):
            print(f" - {topic}")

    except Exception as e:
        print(f"❌ 连接或获取 topic 列表失败: {e}")
        sys.exit(1)


def cmd_cluster_id(args):
    """显示集群 ID"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        client_id=args.client_id or 'kafka-cli-cluster'
    )

    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers,
            client_id=config.client_id
        )
        print("Kafka 集群中的 CLUSTER_ID:", admin_client._client.cluster.cluster_id)
    except Exception as e:
        print(f"❌ 连接或获取 CLUSTER_ID 失败: {e}")
        sys.exit(1)


def cmd_show(args):
    """显示 Topic 详细信息"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'kafka-cli-show'
    )

    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers,
            client_id=config.client_id
        )

        cluster_id = getattr(admin_client._client.cluster, 'cluster_id', 'Unknown')
        print(f"✅ 集群 ID: {cluster_id}\n")

        topic_metadata = admin_client.describe_topics([config.topic_name])

        if not topic_metadata:
            print(f"❌ 无法获取 topic '{config.topic_name}' 的元数据（可能不存在或无权限）")
            sys.exit(1)

        topic_info = topic_metadata[0]
        if topic_info.get("error_code") != 0:
            error_msg = topic_info.get("error_message", "Unknown error")
            print(f"❌ 获取 topic 失败: {error_msg}")
            sys.exit(1)

        print(f"📊 Topic: '{topic_info['topic']}'")
        print(f"分区总数: {len(topic_info['partitions'])}\n")

        for part in sorted(topic_info['partitions'], key=lambda x: x['partition']):
            partition_id = part['partition']
            leader = part['leader']
            replicas = part['replicas']
            isr = part['isr']

            print(f"分区 {partition_id}:")
            print(f"  Leader Broker: {leader}")
            print(f"  副本 (Replicas): {replicas}")
            print(f"  同步副本 (ISR):   {isr}")
            print("-" * 40)

        print("\n📡 Broker 列表:")
        cluster = admin_client._client.cluster
        broker_ids = cluster.brokers()

        if hasattr(cluster, '_brokers'):
            broker_metadata_dict = cluster._brokers
            for bid in sorted(broker_ids):
                bm = broker_metadata_dict.get(bid)
                if bm:
                    print(f"  Broker {bid}: {bm.host}:{bm.port}")
                else:
                    print(f"  Broker {bid}: <metadata not available>")
        else:
            for bid in sorted(broker_ids):
                print(f"  Broker {bid}: <host info unavailable>")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)
    finally:
        admin_client.close()


def cmd_count(args):
    """统计消息数量"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'kafka-cli-count',
        timeout_ms=args.timeout
    )

    try:
        consumer = KafkaConsumer(
            bootstrap_servers=config.bootstrap_servers,
            request_timeout_ms=config.timeout_ms,
            client_id=config.client_id
        )

        partitions = consumer.partitions_for_topic(config.topic_name)
        if partitions is None:
            print(f"❌ Topic '{config.topic_name}' 不存在或无法访问")
            sys.exit(1)

        total_messages = 0
        print(f"正在统计 topic '{config.topic_name}' 的消息数量...")

        for partition_id in partitions:
            tp = TopicPartition(config.topic_name, partition_id)

            beginning_offsets = consumer.beginning_offsets([tp])
            earliest = beginning_offsets[tp]

            end_offsets = consumer.end_offsets([tp])
            latest = end_offsets[tp]

            partition_count = latest - earliest
            total_messages += partition_count

            print(f"  分区 {partition_id}: {partition_count} 条消息 (offset {earliest} → {latest})")

        print(f"\n✅ 总消息数（估算）: {total_messages}")

    except Exception as e:
        print(f"❌ 统计失败: {e}")
        sys.exit(1)
    finally:
        consumer.close()


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


def cmd_export(args):
    """导出消息"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'kafka-cli-export',
        output_file=args.output_file,
        timeout_ms=args.timeout
    )

    output_file = config.output_file
    if not output_file:
        output_file = f'{config.topic_name}.jsonl'

    consumer = KafkaConsumer(
        bootstrap_servers=config.bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=config.timeout_ms,
        client_id=config.client_id
    )

    try:
        partitions = consumer.partitions_for_topic(config.topic_name)
        if not partitions:
            raise RuntimeError(f"Topic {config.topic_name} not found")

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
    except Exception as e:
        print(f"❌ 导出失败: {e}")
        sys.exit(1)
    finally:
        consumer.close()


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


def cmd_import(args):
    """导入消息"""
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        topic_name=args.topic,
        client_id=args.client_id or 'kafka-cli-import',
        input_file=args.input_file
    )

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
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        sys.exit(1)
    finally:
        producer.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Kafka CLI - 统一的 Kafka 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s list -b localhost:9092
  %(prog)s show -t my-topic
  %(prog)s count -t my-topic
  %(prog)s export -t my-topic -o backup.jsonl
  %(prog)s import -t my-topic -i backup.jsonl

环境变量:
  KAFKA_BOOTSTRAP_SERVERS  默认 broker 地址
  KAFKA_TOPIC              默认 topic 名称
  KAFKA_CLIENT_ID          默认客户端 ID
        """
    )

    # 全局参数
    parser.add_argument('-b', '--bootstrap-servers', help=f'Kafka broker 地址 (默认: {KafkaConfig().bootstrap_servers})')
    parser.add_argument('--client-id', help='客户端 ID')

    # 子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # list 命令
    parser_list = subparsers.add_parser('list', help='列出所有 Topics')

    # cluster-id 命令
    parser_cluster = subparsers.add_parser('cluster-id', help='显示集群 ID')

    # show 命令
    parser_show = subparsers.add_parser('show', help='显示 Topic 详细信息')
    parser_show.add_argument('-t', '--topic', required=True, help='Topic 名称')

    # count 命令
    parser_count = subparsers.add_parser('count', help='统计消息数量')
    parser_count.add_argument('-t', '--topic', required=True, help='Topic 名称')
    parser_count.add_argument('--timeout', type=int, help='请求超时时间（毫秒）')

    # export 命令
    parser_export = subparsers.add_parser('export', help='导出消息到文件')
    parser_export.add_argument('-t', '--topic', required=True, help='Topic 名称')
    parser_export.add_argument('-o', '--output-file', help='输出文件路径 (默认: {topic}.jsonl)')
    parser_export.add_argument('--timeout', type=int, help='Consumer 超时时间（毫秒）')

    # import 命令
    parser_import = subparsers.add_parser('import', help='从文件导入消息')
    parser_import.add_argument('-t', '--topic', required=True, help='Topic 名称')
    parser_import.add_argument('-i', '--input-file', help='输入文件路径 (默认: {topic}.jsonl)')
    parser_import.add_argument('--acks', type=int, help='Producer acks 设置')
    parser_import.add_argument('--retries', type=int, help='重试次数')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行对应的命令
    commands = {
        'list': cmd_list,
        'cluster-id': cmd_cluster_id,
        'show': cmd_show,
        'count': cmd_count,
        'export': cmd_export,
        'import': cmd_import,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
