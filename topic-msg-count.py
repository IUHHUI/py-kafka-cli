from kafka import KafkaConsumer
from kafka.structs import TopicPartition

# Kafka 配置
bootstrap_servers = '192.168.220.220:9092'
topic_name = 'prod.hkex.news.ndsdata'

try:
    # 创建一个消费者（不需要订阅，仅用于获取元数据和偏移量）
    consumer = KafkaConsumer(
        bootstrap_servers=bootstrap_servers,
        request_timeout_ms=20000,
        client_id='python-offset-counter'
    )

    # 获取该 topic 的所有分区
    partitions = consumer.partitions_for_topic(topic_name)
    if partitions is None:
        print(f"❌ Topic '{topic_name}' 不存在或无法访问")
        exit(1)

    total_messages = 0
    print(f"正在统计 topic '{topic_name}' 的消息数量...")

    for partition_id in partitions:
        tp = TopicPartition(topic_name, partition_id)
        
        # 获取 earliest offset（起始）
        beginning_offsets = consumer.beginning_offsets([tp])
        earliest = beginning_offsets[tp]

        # 获取 latest offset（结束，注意：latest 是下一个将要写入的 offset）
        end_offsets = consumer.end_offsets([tp])
        latest = end_offsets[tp]

        partition_count = latest - earliest
        total_messages += partition_count

        print(f"  分区 {partition_id}: {partition_count} 条消息 (offset {earliest} → {latest})")

    print(f"\n✅ 总消息数（估算）: {total_messages}")

except Exception as e:
    print(f"❌ 统计失败: {e}")
finally:
    consumer.close()
