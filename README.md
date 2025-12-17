# Kafka Python CLI 工具

一套用于管理和操作 Kafka 的 Python 命令行工具集。

## 功能特性

- 统一的参数命名规范
- 命令行参数支持
- 环境变量配置支持
- 灵活的配置管理

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

### 配置优先级

配置按以下优先级加载（从高到低）：

1. **命令行参数** - 直接在命令行指定
2. **环境变量** - 通过环境变量设置
3. **默认值** - 代码中的默认配置

### 环境变量

可以通过以下环境变量设置默认配置：

```bash
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
export KAFKA_TOPIC="your-topic-name"
export KAFKA_CLIENT_ID="my-kafka-client"
export KAFKA_CONSUMER_GROUP="my-consumer-group"
export KAFKA_TIMEOUT_MS="20000"
export KAFKA_ACKS="1"
export KAFKA_RETRIES="3"
```

## 工具列表

### 1. topic-list.py - 列出所有 Topics

列出 Kafka 集群中的所有 Topics。

**使用方法：**

```bash
# 使用默认配置
python topic-list.py

# 指定 broker 地址
python topic-list.py -b localhost:9092

# 使用完整参数
python topic-list.py --bootstrap-servers localhost:9092 --client-id my-client
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `--client-id`: 客户端 ID

### 2. show-cluster-id.py - 显示集群 ID

显示 Kafka 集群的 Cluster ID。

**使用方法：**

```bash
# 使用默认配置
python show-cluster-id.py

# 指定 broker 地址
python show-cluster-id.py -b localhost:9092
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `--client-id`: 客户端 ID

### 3. topic-show.py - 显示 Topic 详细信息

显示指定 Topic 的详细信息，包括分区、副本、ISR 等。

**使用方法：**

```bash
# 查看指定 topic
python topic-show.py -t prod.hkex.news.ndsdata

# 指定 broker 和 topic
python topic-show.py -b localhost:9092 -t my-topic
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `-t, --topic`: Topic 名称（必填）
- `--client-id`: 客户端 ID

### 4. topic-msg-count.py - 统计消息数量

统计指定 Topic 中的消息总数。

**使用方法：**

```bash
# 统计指定 topic 的消息数
python topic-msg-count.py -t prod.hkex.news.ndsdata

# 指定 broker 和超时时间
python topic-msg-count.py -b localhost:9092 -t my-topic --timeout 30000
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `-t, --topic`: Topic 名称（必填）
- `--client-id`: 客户端 ID
- `--timeout`: 请求超时时间（毫秒）

### 5. topic-export.py - 导出消息

将 Kafka Topic 中的消息导出到 JSONL 文件。

**使用方法：**

```bash
# 导出到默认文件 {topic}.jsonl
python topic-export.py -t prod.hkex.news.ndsdata

# 指定输出文件
python topic-export.py -t my-topic -o /path/to/output.jsonl

# 完整参数
python topic-export.py -b localhost:9092 -t my-topic -o data.jsonl --timeout 30000
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `-t, --topic`: Topic 名称（必填）
- `-o, --output-file`: 输出文件路径（默认：{topic}.jsonl）
- `--client-id`: 客户端 ID
- `--timeout`: Consumer 超时时间（毫秒）

### 6. topic-import.py - 导入消息

从 JSONL 文件导入消息到 Kafka Topic。

**使用方法：**

```bash
# 从默认文件 {topic}.jsonl 导入
python topic-import.py -t prod.hkex.news.ndsdata

# 指定输入文件
python topic-import.py -t my-topic -i /path/to/input.jsonl

# 完整参数
python topic-import.py -b localhost:9092 -t my-topic -i data.jsonl --acks 1 --retries 3
```

**参数说明：**

- `-b, --bootstrap-servers`: Kafka broker 地址
- `-t, --topic`: Topic 名称（必填）
- `-i, --input-file`: 输入文件路径（默认：{topic}.jsonl）
- `--client-id`: 客户端 ID
- `--acks`: Producer acks 设置
- `--retries`: 重试次数

## 统一的参数命名规范

所有工具现在使用统一的参数命名：

| 参数用途 | Python 变量名 | 环境变量 | 命令行参数 |
|---------|--------------|---------|-----------|
| Kafka Broker 地址 | `bootstrap_servers` | `KAFKA_BOOTSTRAP_SERVERS` | `-b, --bootstrap-servers` |
| Topic 名称 | `topic_name` | `KAFKA_TOPIC` | `-t, --topic` |
| 客户端 ID | `client_id` | `KAFKA_CLIENT_ID` | `--client-id` |
| 消费者组 | `consumer_group` | `KAFKA_CONSUMER_GROUP` | `--consumer-group` |
| 超时时间 | `timeout_ms` | `KAFKA_TIMEOUT_MS` | `--timeout` |
| Producer ACKs | `acks` | `KAFKA_ACKS` | `--acks` |
| 重试次数 | `retries` | `KAFKA_RETRIES` | `--retries` |

## 配置管理

项目包含一个统一的配置管理模块 `config.py`，所有工具都使用这个模块来管理配置。

### KafkaConfig 类

```python
from config import KafkaConfig

# 使用默认配置
config = KafkaConfig()

# 从命令行参数创建配置
config = KafkaConfig.from_cli_args(
    bootstrap_servers='localhost:9092',
    topic_name='my-topic'
)
```

## 示例场景

### 场景 1: 备份和恢复 Topic 数据

```bash
# 1. 导出数据
python topic-export.py -b prod-kafka:9092 -t my-important-topic -o backup.jsonl

# 2. 导入到测试环境
python topic-import.py -b test-kafka:9092 -t my-test-topic -i backup.jsonl
```

### 场景 2: 监控和统计

```bash
# 1. 查看所有 topics
python topic-list.py -b prod-kafka:9092

# 2. 查看特定 topic 的详情
python topic-show.py -b prod-kafka:9092 -t my-topic

# 3. 统计消息数量
python topic-msg-count.py -b prod-kafka:9092 -t my-topic
```

### 场景 3: 使用环境变量简化命令

```bash
# 设置环境变量
export KAFKA_BOOTSTRAP_SERVERS="prod-kafka:9092"
export KAFKA_TOPIC="my-topic"

# 现在可以使用更简洁的命令
python topic-show.py -t my-topic
python topic-msg-count.py -t my-topic
python topic-export.py -t my-topic
```

## 获取帮助

每个工具都支持 `-h` 或 `--help` 参数来查看详细的帮助信息：

```bash
python topic-list.py --help
python topic-export.py --help
python topic-import.py --help
```

## 注意事项

1. 导出大量数据时，建议使用 `--timeout` 参数增加超时时间
2. 导入数据时，默认每 1000 条消息显示一次进度
3. 所有工具都会自动处理异常并显示友好的错误信息
4. 默认的 bootstrap_servers 是 `localhost:9092`，可以通过参数或环境变量修改
