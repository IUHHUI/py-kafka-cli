from kafka.admin import KafkaAdminClient

# Kafka broker 地址
bootstrap_servers = '192.168.220.220:9092'

try:
    # 创建 Admin 客户端
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id='python-topic-list-demo'
    )

    # 获取所有 topic 名称
    topic_list = admin_client.list_topics()
    
    print("Kafka 集群中的 Topics:")
    for topic in sorted(topic_list):
        print(f" - {topic}")

except Exception as e:
    print(f"❌ 连接或获取 topic 列表失败: {e}")
