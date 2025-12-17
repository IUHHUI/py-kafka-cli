"""
Kafka CLI 统一配置管理模块
提供环境变量和默认值支持
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class KafkaConfig:
    """Kafka 配置类，支持环境变量和默认值"""

    # Kafka 连接配置
    bootstrap_servers: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

    # Topic 配置
    topic_name: Optional[str] = os.getenv('KAFKA_TOPIC', None)

    # 客户端配置
    client_id: str = os.getenv('KAFKA_CLIENT_ID', 'py-kafka-cli')
    consumer_group: str = os.getenv('KAFKA_CONSUMER_GROUP', 'py-kafka-cli-group')

    # 超时配置
    timeout_ms: int = int(os.getenv('KAFKA_TIMEOUT_MS', '20000'))

    # Producer 配置
    acks: int = int(os.getenv('KAFKA_ACKS', '1'))
    retries: int = int(os.getenv('KAFKA_RETRIES', '3'))

    # 文件配置
    output_file: Optional[str] = None
    input_file: Optional[str] = None

    def __post_init__(self):
        """初始化后处理，设置默认文件名"""
        if self.output_file is None and self.topic_name:
            self.output_file = f"{self.topic_name}.jsonl"
        if self.input_file is None and self.topic_name:
            self.input_file = f"{self.topic_name}.jsonl"

    @classmethod
    def from_cli_args(cls, bootstrap_servers: Optional[str] = None,
                      topic_name: Optional[str] = None,
                      client_id: Optional[str] = None,
                      consumer_group: Optional[str] = None,
                      timeout_ms: Optional[int] = None,
                      output_file: Optional[str] = None,
                      input_file: Optional[str] = None):
        """从命令行参数创建配置对象，命令行参数优先级最高"""
        config = cls()

        if bootstrap_servers is not None:
            config.bootstrap_servers = bootstrap_servers
        if topic_name is not None:
            config.topic_name = topic_name
        if client_id is not None:
            config.client_id = client_id
        if consumer_group is not None:
            config.consumer_group = consumer_group
        if timeout_ms is not None:
            config.timeout_ms = timeout_ms
        if output_file is not None:
            config.output_file = output_file
        if input_file is not None:
            config.input_file = input_file

        # 更新默认文件名
        config.__post_init__()

        return config


# 默认配置实例
default_config = KafkaConfig()
