import argparse
from kafka.admin import KafkaAdminClient
from config import KafkaConfig


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='列出 Kafka 集群中的所有 Topics')
    parser.add_argument(
        '-b', '--bootstrap-servers',
        type=str,
        help=f'Kafka broker 地址 (默认: {KafkaConfig().bootstrap_servers})'
    )
    parser.add_argument(
        '--client-id',
        type=str,
        help='客户端 ID (默认: python-topic-list-demo)'
    )
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 从命令行参数创建配置
    config = KafkaConfig.from_cli_args(
        bootstrap_servers=args.bootstrap_servers,
        client_id=args.client_id or 'python-topic-list-demo'
    )

    try:
        # 创建 Admin 客户端
        admin_client = KafkaAdminClient(
            bootstrap_servers=config.bootstrap_servers,
            client_id=config.client_id
        )

        # 获取所有 topic 名称
        topic_list = admin_client.list_topics()

        print("Kafka 集群中的 Topics:")
        for topic in sorted(topic_list):
            print(f" - {topic}")

    except Exception as e:
        print(f"❌ 连接或获取 topic 列表失败: {e}")


if __name__ == '__main__':
    main()
