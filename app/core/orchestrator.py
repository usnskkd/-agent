from __future__ import annotations

from app.core.agents import AgentContext, build_default_agents


class MultiAgentOrchestrator:
    def __init__(self):
        self.agents = build_default_agents()

    def run(self, task: dict) -> dict:
        context = AgentContext(
            goal=task["goal"],
            channel=task["channel"],
            audience=task["audience"],
            budget=task["budget"],
            extra=task.get("metadata", {}),
        )
        outputs: dict[str, dict] = {}
        timeline: list[dict] = []

        for agent in self.agents:
            result = agent.run(context, outputs)
            outputs[agent.name] = result
            timeline.append(
                {
                    "agent": agent.name,
                    "role": agent.role,
                    "output": result,
                }
            )

        return {
            "summary": {
                "goal": task["goal"],
                "channel": task["channel"],
                "status": outputs["publisher"]["final_status"],
                "review_score": outputs["reviewer"]["score"],
            },
            "timeline": timeline,
            "artifacts": outputs,
        }


orchestrator = MultiAgentOrchestrator()
