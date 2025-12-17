# Kafka Python CLI 工具

一套用于管理和操作 Kafka 的 Python 命令行工具集。

## 功能特性

- 统一的参数命名规范
- 命令行参数支持
- 环境变量配置支持
- 灵活的配置管理
- **支持编译为单一可执行文件**，无需 Python 环境即可运行

## 快速开始

### 方式 1: 使用编译后的可执行文件（推荐）

**构建单一可执行文件：**

```bash
# Linux/macOS
./build.sh

# Windows
build.bat
```

构建完成后，可执行文件位于 `dist/kafka-cli` (Linux/macOS) 或 `dist/kafka-cli.exe` (Windows)

**使用可执行文件：**

```bash
# Linux/macOS
./dist/kafka-cli --help
./dist/kafka-cli list -b localhost:9092
./dist/kafka-cli show -t my-topic

# Windows
dist\kafka-cli.exe --help
dist\kafka-cli.exe list -b localhost:9092
dist\kafka-cli.exe show -t my-topic

# 或者复制到系统路径后直接使用
kafka-cli --help
```

### 方式 2: 使用 Python 直接运行

**安装依赖：**

```bash
pip install -r requirements.txt
```

**使用统一的 CLI 入口：**

```bash
# 使用 kafka_cli.py 作为统一入口
python kafka_cli.py --help
python kafka_cli.py list -b localhost:9092
python kafka_cli.py show -t my-topic
```

**或使用独立脚本：**

```bash
python topic-list.py
python topic-show.py -t my-topic
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

## 统一 CLI 命令参考

`kafka-cli` (或 `kafka_cli.py`) 提供了统一的命令行界面，所有功能通过子命令访问。

### 命令格式

```bash
kafka-cli [全局选项] <子命令> [子命令选项]
```

### 全局选项

- `-b, --bootstrap-servers`: Kafka broker 地址
- `--client-id`: 客户端 ID
- `-h, --help`: 显示帮助信息

### 可用子命令

| 子命令 | 说明 | 示例 |
|--------|------|------|
| `list` | 列出所有 Topics | `kafka-cli list` |
| `cluster-id` | 显示集群 ID | `kafka-cli cluster-id` |
| `show` | 显示 Topic 详细信息 | `kafka-cli show -t my-topic` |
| `count` | 统计消息数量 | `kafka-cli count -t my-topic` |
| `export` | 导出消息到文件 | `kafka-cli export -t my-topic -o data.jsonl` |
| `import` | 从文件导入消息 | `kafka-cli import -t my-topic -i data.jsonl` |

### 使用示例

```bash
# 列出所有 topics
kafka-cli list -b localhost:9092

# 显示集群 ID
kafka-cli cluster-id -b localhost:9092

# 查看 topic 详细信息
kafka-cli show -b localhost:9092 -t my-topic

# 统计消息数量
kafka-cli count -b localhost:9092 -t my-topic

# 导出消息
kafka-cli export -b localhost:9092 -t my-topic -o backup.jsonl

# 导入消息
kafka-cli import -b localhost:9092 -t my-topic -i backup.jsonl

# 使用环境变量简化命令
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
kafka-cli list
kafka-cli show -t my-topic
kafka-cli export -t my-topic
```

## 独立脚本工具列表

除了统一的 CLI，也可以直接使用独立的 Python 脚本：

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

## 构建和部署

### 构建单一可执行文件

项目提供了自动化构建脚本，可以将工具打包成单一的可执行文件，方便在不同机器上部署。

**Linux/macOS 构建：**

```bash
# 赋予执行权限
chmod +x build.sh

# 执行构建
./build.sh
```

**Windows 构建：**

```cmd
build.bat
```

**构建产物：**

- Linux/macOS: `dist/kafka-cli`
- Windows: `dist/kafka-cli.exe`

### 部署到其他机器

构建后的可执行文件是**完全独立**的，可以直接复制到其他机器使用，无需安装 Python 或任何依赖。

**Linux/macOS 部署：**

```bash
# 复制到目标机器
scp dist/kafka-cli user@remote-host:/path/to/destination/

# 在目标机器上直接运行
./kafka-cli --help

# 或者安装到系统路径
sudo cp kafka-cli /usr/local/bin/
kafka-cli --help
```

**Windows 部署：**

```cmd
# 复制 dist\kafka-cli.exe 到目标机器
# 直接运行
kafka-cli.exe --help

# 或添加到 PATH 环境变量后使用
kafka-cli --help
```

### 构建详细说明

**构建流程：**

1. 检查 Python 环境
2. 安装项目依赖（包括 PyInstaller）
3. 清理旧的构建文件
4. 使用 PyInstaller 打包
5. 生成单一可执行文件

**自定义构建：**

如果需要自定义构建选项，可以编辑 `kafka-cli.spec` 文件：

```python
# kafka-cli.spec
exe = EXE(
    ...
    name='kafka-cli',        # 可执行文件名称
    debug=False,             # 是否启用调试模式
    upx=True,                # 是否使用 UPX 压缩
    console=True,            # 是否显示控制台窗口
    ...
)
```

然后手动运行构建：

```bash
pyinstaller kafka-cli.spec --clean
```

### 文件大小

编译后的可执行文件大小约为 **15-25 MB**（取决于平台和 UPX 压缩）。

### 系统要求

**开发环境（用于构建）：**
- Python 3.7+
- pip

**运行环境（使用可执行文件）：**
- 无需任何依赖，直接运行即可
- 支持 Linux、macOS、Windows

## 注意事项

1. 导出大量数据时，建议使用 `--timeout` 参数增加超时时间
2. 导入数据时，默认每 1000 条消息显示一次进度
3. 所有工具都会自动处理异常并显示友好的错误信息
4. 默认的 bootstrap_servers 是 `localhost:9092`，可以通过参数或环境变量修改
5. 编译后的可执行文件包含所有依赖，可以在没有 Python 环境的机器上运行
6. 首次运行可执行文件时，可能需要几秒钟的初始化时间

## 项目结构

```
py-kafka-cli/
├── config.py              # 统一配置管理模块
├── kafka_cli.py           # 统一 CLI 入口（推荐使用）
├── topic-list.py          # 独立脚本：列出 topics
├── show-cluster-id.py     # 独立脚本：显示集群 ID
├── topic-show.py          # 独立脚本：显示 topic 详情
├── topic-msg-count.py     # 独立脚本：统计消息数量
├── topic-export.py        # 独立脚本：导出消息
├── topic-import.py        # 独立脚本：导入消息
├── kafka-cli.spec         # PyInstaller 配置文件
├── build.sh               # Linux/macOS 构建脚本
├── build.bat              # Windows 构建脚本
├── requirements.txt       # Python 依赖列表
└── README.md              # 项目文档
```

## 故障排除

### 构建失败

**问题：** `ModuleNotFoundError: No module named 'PyInstaller'`

**解决：** 确保已安装 PyInstaller
```bash
pip install pyinstaller
```

**问题：** 构建时提示找不到某些模块

**解决：** 编辑 `kafka-cli.spec`，在 `hiddenimports` 中添加缺失的模块

### 运行问题

**问题：** 可执行文件无法运行或启动很慢

**解决：**
- 首次运行时需要解压临时文件，会稍慢，后续会快很多
- 确保有足够的磁盘空间和临时目录权限
- 在 Linux 上确保文件有执行权限：`chmod +x kafka-cli`

**问题：** 连接 Kafka 失败

**解决：**
- 检查 bootstrap-servers 地址是否正确
- 确保网络可达
- 检查防火墙设置
- 使用 `-b` 参数或环境变量 `KAFKA_BOOTSTRAP_SERVERS` 指定正确的地址
