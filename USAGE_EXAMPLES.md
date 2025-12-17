# Kafka CLI 使用示例

本文档提供了 Kafka CLI 工具的实际使用示例。

## 基本使用

### 1. 列出所有 Topics

```bash
# 使用可执行文件
kafka-cli list -b localhost:9092

# 或使用 Python
python kafka_cli.py list -b localhost:9092
```

**输出示例：**
```
Kafka 集群中的 Topics:
 - my-topic-1
 - my-topic-2
 - prod.hkex.news.ndsdata
```

### 2. 查看集群信息

```bash
kafka-cli cluster-id -b localhost:9092
```

**输出示例：**
```
Kafka 集群中的 CLUSTER_ID: xtzWWN4bTjitpL3kfd9s5g
```

### 3. 查看 Topic 详细信息

```bash
kafka-cli show -b localhost:9092 -t my-topic
```

**输出示例：**
```
✅ 集群 ID: xtzWWN4bTjitpL3kfd9s5g

📊 Topic: 'my-topic'
分区总数: 3

分区 0:
  Leader Broker: 1
  副本 (Replicas): [1, 2, 3]
  同步副本 (ISR):   [1, 2, 3]
----------------------------------------
分区 1:
  Leader Broker: 2
  副本 (Replicas): [2, 3, 1]
  同步副本 (ISR):   [2, 3, 1]
----------------------------------------
分区 2:
  Leader Broker: 3
  副本 (Replicas): [3, 1, 2]
  同步副本 (ISR):   [3, 1, 2]
----------------------------------------

📡 Broker 列表:
  Broker 1: kafka1.example.com:9092
  Broker 2: kafka2.example.com:9092
  Broker 3: kafka3.example.com:9092
```

### 4. 统计消息数量

```bash
kafka-cli count -b localhost:9092 -t my-topic
```

**输出示例：**
```
正在统计 topic 'my-topic' 的消息数量...
  分区 0: 15234 条消息 (offset 0 → 15234)
  分区 1: 14987 条消息 (offset 0 → 14987)
  分区 2: 15456 条消息 (offset 0 → 15456)

✅ 总消息数（估算）: 45677
```

## 数据导入导出

### 5. 导出 Topic 数据

**导出到默认文件：**

```bash
# 导出到 {topic}.jsonl
kafka-cli export -b localhost:9092 -t my-topic
```

**导出到指定文件：**

```bash
kafka-cli export -b localhost:9092 -t my-topic -o /backup/my-topic-backup.jsonl
```

**输出示例：**
```
开始导出 topic 'my-topic' 共 3 个分区...
已导出 1000 条消息...
已导出 2000 条消息...
已导出 3000 条消息...
✅ 导出完成！共 3245 条消息，保存到 my-topic.jsonl
```

### 6. 导入 Topic 数据

**从默认文件导入：**

```bash
# 从 {topic}.jsonl 导入
kafka-cli import -b localhost:9092 -t my-new-topic
```

**从指定文件导入：**

```bash
kafka-cli import -b localhost:9092 -t my-new-topic -i /backup/my-topic-backup.jsonl
```

**输出示例：**
```
已导入 1000 条消息...
已导入 2000 条消息...
已导入 3000 条消息...
✅ 导入完成！共 3245 条消息到 topic 'my-new-topic'
```

## 高级用法

### 7. 使用环境变量

设置环境变量以简化命令：

```bash
# 设置环境变量
export KAFKA_BOOTSTRAP_SERVERS="prod-kafka.example.com:9092"
export KAFKA_TOPIC="my-default-topic"

# 现在可以省略常用参数
kafka-cli list
kafka-cli show -t my-topic
kafka-cli count -t my-topic
```

### 8. Topic 数据备份和恢复

**场景：备份生产环境 Topic 到测试环境**

```bash
# 步骤 1: 从生产环境导出
kafka-cli export \
  -b prod-kafka:9092 \
  -t prod.orders \
  -o orders-backup-2024-01-15.jsonl

# 步骤 2: 导入到测试环境
kafka-cli import \
  -b test-kafka:9092 \
  -t test.orders \
  -i orders-backup-2024-01-15.jsonl
```

### 9. 数据迁移

**场景：迁移 Topic 到新集群**

```bash
# 导出原集群数据
kafka-cli export \
  -b old-cluster:9092 \
  -t important-topic \
  -o migration.jsonl

# 导入到新集群
kafka-cli import \
  -b new-cluster:9092 \
  -t important-topic \
  -i migration.jsonl \
  --acks all \
  --retries 5
```

### 10. 批量操作

**场景：导出多个 Topics**

```bash
#!/bin/bash
# export-all-topics.sh

BROKER="localhost:9092"
TOPICS=("topic1" "topic2" "topic3")

for topic in "${TOPICS[@]}"; do
  echo "导出 $topic..."
  kafka-cli export -b $BROKER -t $topic -o "${topic}.jsonl"
done

echo "所有 topics 导出完成！"
```

### 11. 监控脚本

**场景：定期检查 Topic 消息数量**

```bash
#!/bin/bash
# monitor-topics.sh

BROKER="localhost:9092"
TOPICS=("orders" "payments" "users")

while true; do
  clear
  echo "=== Kafka Topics 监控 ==="
  echo "时间: $(date)"
  echo ""

  for topic in "${TOPICS[@]}"; do
    echo "Topic: $topic"
    kafka-cli count -b $BROKER -t $topic | grep "总消息数"
    echo ""
  done

  sleep 60
done
```

### 12. 大数据量导出

**场景：导出大量数据，增加超时时间**

```bash
# 增加超时到 60 秒
kafka-cli export \
  -b localhost:9092 \
  -t large-topic \
  -o large-data.jsonl \
  --timeout 60000
```

## Windows 使用示例

### 使用可执行文件

```cmd
REM 列出 topics
kafka-cli.exe list -b localhost:9092

REM 导出数据
kafka-cli.exe export -b localhost:9092 -t my-topic -o C:\backup\my-topic.jsonl

REM 导入数据
kafka-cli.exe import -b localhost:9092 -t new-topic -i C:\backup\my-topic.jsonl
```

### 使用 PowerShell

```powershell
# 设置环境变量
$env:KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# 批量导出
$topics = @("topic1", "topic2", "topic3")
foreach ($topic in $topics) {
    Write-Host "导出 $topic..."
    kafka-cli.exe export -t $topic -o "$topic.jsonl"
}
```

## 故障排查示例

### 连接问题

```bash
# 测试连接
kafka-cli cluster-id -b localhost:9092

# 如果失败，尝试不同的地址
kafka-cli cluster-id -b 127.0.0.1:9092
kafka-cli cluster-id -b kafka.local:9092
```

### 超时问题

```bash
# 如果默认超时不够，增加超时时间
kafka-cli count -b localhost:9092 -t my-topic --timeout 30000
kafka-cli export -b localhost:9092 -t my-topic --timeout 60000
```

### 调试导出的数据格式

```bash
# 导出数据
kafka-cli export -b localhost:9092 -t test-topic -o test.jsonl

# 查看第一条消息
head -n 1 test.jsonl | jq .

# 查看消息结构
head -n 1 test.jsonl | jq 'keys'
```

## 最佳实践

1. **备份前先检查**
   ```bash
   # 先统计消息数量
   kafka-cli count -b prod:9092 -t important-topic

   # 再执行导出
   kafka-cli export -b prod:9092 -t important-topic -o backup.jsonl
   ```

2. **使用有意义的文件名**
   ```bash
   DATE=$(date +%Y%m%d)
   kafka-cli export -b prod:9092 -t orders -o "orders-backup-${DATE}.jsonl"
   ```

3. **验证导入结果**
   ```bash
   # 导入前记录消息数
   kafka-cli count -b test:9092 -t target-topic

   # 执行导入
   kafka-cli import -b test:9092 -t target-topic -i backup.jsonl

   # 导入后验证
   kafka-cli count -b test:9092 -t target-topic
   ```

4. **使用配置文件（通过环境变量）**
   ```bash
   # 创建 .env 文件
   cat > kafka.env << EOF
   export KAFKA_BOOTSTRAP_SERVERS="prod-kafka:9092"
   export KAFKA_CLIENT_ID="backup-tool"
   EOF

   # 使用配置
   source kafka.env
   kafka-cli list
   ```
