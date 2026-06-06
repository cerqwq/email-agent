"""
Email Agent - AI邮件助手
支持邮件分类、摘要、自动回复
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass, field

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


@dataclass
class Email:
    """邮件"""
    id: str
    sender: str
    to: str
    subject: str
    body: str
    date: datetime = field(default_factory=datetime.now)
    is_read: bool = False
    category: str = ""
    priority: str = "normal"


class EmailAgent:
    """
    AI邮件助手
    支持：分类、摘要、回复建议、优先级判断
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        self.emails: List[Email] = []
        self.categories = ["工作", "个人", "推广", "通知", "垃圾"]

        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def add_email(self, email: Email):
        """添加邮件"""
        self.emails.append(email)

    def classify_email(self, email: Email) -> str:
        """分类邮件"""
        if not self.client:
            return "未知"

        prompt = f"""请将以下邮件分类到最合适的类别：

发件人：{email.sender}
主题：{email.subject}
内容：{email.body[:200]}

类别：{', '.join(self.categories)}

只返回类别名称："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        category = response.choices[0].message.content.strip()
        email.category = category
        return category

    def summarize_email(self, email: Email) -> str:
        """邮件摘要"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请用1-2句话总结以下邮件：

发件人：{email.sender}
主题：{email.subject}
内容：{email.body}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return response.choices[0].message.content

    def suggest_reply(self, email: Email, tone: str = "professional") -> str:
        """建议回复"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下邮件建议回复：

发件人：{email.sender}
主题：{email.subject}
内容：{email.body}

语气：{tone}

请生成一个合适的回复："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        return response.choices[0].message.content

    def judge_priority(self, email: Email) -> str:
        """判断优先级"""
        if not self.client:
            return "normal"

        prompt = f"""请判断以下邮件的优先级：

发件人：{email.sender}
主题：{email.subject}
内容：{email.body[:200]}

优先级：high/medium/low

只返回优先级："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )

        priority = response.choices[0].message.content.strip().lower()
        email.priority = priority if priority in ["high", "medium", "low"] else "normal"
        return email.priority

    def batch_process(self, emails: List[Email] = None) -> List[Dict]:
        """批量处理邮件"""
        emails = emails or self.emails
        results = []

        for email in emails:
            result = {
                "id": email.id,
                "subject": email.subject,
                "sender": email.sender,
                "category": self.classify_email(email),
                "priority": self.judge_priority(email),
                "summary": self.summarize_email(email)
            }
            results.append(result)

        return results

    def get_stats(self) -> Dict:
        """获取统计"""
        category_counts = {}
        priority_counts = {"high": 0, "medium": 0, "low": 0, "normal": 0}

        for email in self.emails:
            cat = email.category or "未分类"
            category_counts[cat] = category_counts.get(cat, 0) + 1
            priority_counts[email.priority] = priority_counts.get(email.priority, 0) + 1

        return {
            "total_emails": len(self.emails),
            "categories": category_counts,
            "priorities": priority_counts
        }


def create_agent(**kwargs) -> EmailAgent:
    """创建邮件Agent"""
    return EmailAgent(**kwargs)


if __name__ == "__main__":
    agent = create_agent()

    print("Email Agent")
    print()

    # 测试邮件
    test_emails = [
        Email(
            id="1",
            sender="boss@company.com",
            to="me@company.com",
            subject="项目进度报告",
            body="请在周五前提交项目进度报告，包括本周完成的工作和下周计划。"
        ),
        Email(
            id="2",
            sender="newsletter@shop.com",
            to="me@company.com",
            subject="限时优惠！全场5折",
            body="尊敬的用户，我们正在进行限时促销活动，所有商品5折优惠。"
        ),
        Email(
            id="3",
            sender="friend@gmail.com",
            to="me@company.com",
            subject="周末聚会",
            body="嗨，周末有空吗？想约你一起吃饭。"
        ),
    ]

    for email in test_emails:
        print(f"Processing: {email.subject}")
        print(f"  Category: {agent.classify_email(email)}")
        print(f"  Priority: {agent.judge_priority(email)}")
        print(f"  Summary: {agent.summarize_email(email)}")
        print()
