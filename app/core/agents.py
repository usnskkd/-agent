from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentContext:
    goal: str
    channel: str
    audience: str
    budget: str
    extra: dict


class BaseAgent:
    name = "base"
    role = "generic"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        raise NotImplementedError


class PlannerAgent(BaseAgent):
    name = "planner"
    role = "目标拆解与执行策略"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        return {
            "objective": context.goal,
            "channel": context.channel,
            "phases": [
                "目标拆解",
                "内容准备",
                "质量审核",
                "发布时间安排",
                "复盘指标跟踪",
            ],
            "priority": "high",
            "generated_at": datetime.utcnow().isoformat(),
        }


class ResearcherAgent(BaseAgent):
    name = "researcher"
    role = "素材研究与渠道建议"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        return {
            "insights": [
                f"{context.channel} 适合短周期测试和高频迭代",
                f"目标人群 {context.audience} 更关注明确收益和行动指引",
                "建议采用 3 组内容角度并行测试",
            ],
            "competitor_patterns": [
                "问题切入",
                "案例证明",
                "限时行动",
            ],
        }


class CopywriterAgent(BaseAgent):
    name = "copywriter"
    role = "内容生成"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        insights = upstream.get("researcher", {}).get("insights", [])
        angle = insights[0] if insights else "围绕核心价值输出"
        return {
            "headline": f"{context.goal}：用更短路径拿到更稳结果",
            "body": (
                f"面向 {context.audience}，本次重点在 {context.channel} 完成转化闭环。"
                f"执行建议：{angle}。预算策略为 {context.budget}，先小流量验证，再逐步放大。"
            ),
            "cta": "立即预约/咨询/领取方案",
        }


class ReviewerAgent(BaseAgent):
    name = "reviewer"
    role = "风控与质量审查"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        body = upstream.get("copywriter", {}).get("body", "")
        risks = []
        if "绝对" in body or "保证" in body:
            risks.append("存在绝对化表达风险")
        return {
            "approved": len(risks) == 0,
            "risks": risks or ["未发现明显风险"],
            "score": 92 if not risks else 70,
        }


class PublisherAgent(BaseAgent):
    name = "publisher"
    role = "发布编排与交付"

    def run(self, context: AgentContext, upstream: dict) -> dict:
        return {
            "publish_plan": [
                f"T+0 在 {context.channel} 发布首条内容",
                "T+1 根据互动率调整标题",
                "T+2 放大高互动版本",
            ],
            "final_status": "ready" if upstream.get("reviewer", {}).get("approved") else "hold",
        }


def build_default_agents() -> list[BaseAgent]:
    return [
        PlannerAgent(),
        ResearcherAgent(),
        CopywriterAgent(),
        ReviewerAgent(),
        PublisherAgent(),
    ]
