from kafka.admin import KafkaAdminClient

# Kafka broker 地址
bootstrap_servers = '127.0.0.1:9092'

try:
    # 创建 Admin 客户端
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id='python-topic-list-demo'
    )
    print("Kafka 集群中的 CLUSTER_ID:", admin_client._client.cluster.cluster_id)
except Exception as e:
    print(f"❌ 连接或获取 CLUSTER_ID 失败: {e}")
