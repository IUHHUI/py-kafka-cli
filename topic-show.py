from kafka.admin import KafkaAdminClient

bootstrap_servers = '192.168.220.220:9092'
topic_name = 'prod.hkex.news.ndsdata'

try:
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id='topic-metadata-safe-demo'
    )

    # 获取集群 ID（通过内部属性，但仅用于展示）
    cluster_id = getattr(admin_client._client.cluster, 'cluster_id', 'Unknown')
    print(f"✅ 集群 ID: {cluster_id}\n")

    # 使用 describe_topics 获取 topic 详细信息
    topic_metadata = admin_client.describe_topics([topic_name])

    if not topic_metadata:
        print(f"❌ 无法获取 topic '{topic_name}' 的元数据（可能不存在或无权限）")
        exit(1)

    topic_info = topic_metadata[0]
    if topic_info.get("error_code") != 0:
        error_msg = topic_info.get("error_message", "Unknown error")
        print(f"❌ 获取 topic 失败: {error_msg}")
        exit(1)

    print(f"📊 Topic: '{topic_info['topic']}'")
    print(f"分区总数: {len(topic_info['partitions'])}\n")

    # 遍历每个分区
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

    # ✅ 修复：安全获取 Broker 列表（兼容 kafka-python 2.x）
    print("\n📡 Broker 列表:")
    cluster = admin_client._client.cluster

    # 方法：遍历所有 broker IDs，并获取其元数据
    # 在 kafka-python 2.x 中，cluster.brokers() 返回 set of broker IDs
    broker_ids = cluster.brokers()
    if hasattr(cluster, '_brokers'):
        # _brokers 是 {broker_id: BrokerMetadata} 的字典
        broker_metadata_dict = cluster._brokers
        for bid in sorted(broker_ids):
            bm = broker_metadata_dict.get(bid)
            if bm:
                print(f"  Broker {bid}: {bm.host}:{bm.port}")
            else:
                print(f"  Broker {bid}: <metadata not available>")
    else:
        # 回退：仅打印 ID（极端情况）
        for bid in sorted(broker_ids):
            print(f"  Broker {bid}: <host info unavailable>")

except Exception as e:
    print(f"❌ 发生错误: {e}")
finally:
    admin_client.close()
