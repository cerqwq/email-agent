# 📧 Email Agent

AI邮件助手，支持邮件分类、摘要、自动回复。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🏷️ 邮件自动分类
- 📝 邮件摘要
- 💬 回复建议
- ⚡ 优先级判断
- 📊 批量处理

## 🚀 快速开始

```bash
pip install openai

python agent.py
```

## 📖 使用

```python
from email_agent import create_agent, Email

agent = create_agent()

# 添加邮件
email = Email(
    id="1",
    sender="boss@company.com",
    to="me@company.com",
    subject="项目进度",
    body="请提交项目进度报告"
)

# 分类
category = agent.classify_email(email)

# 摘要
summary = agent.summarize_email(email)

# 回复建议
reply = agent.suggest_reply(email, tone="professional")

# 优先级
priority = agent.judge_priority(email)

# 批量处理
results = agent.batch_process([email1, email2, email3])
```

## 📁 项目结构

```
email-agent/
├── agent.py       # 邮件Agent核心
└── README.md
```

## 📄 许可证

MIT License
