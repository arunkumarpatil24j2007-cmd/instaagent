"""
Critique Schema for Instagram Specialist Agent.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List


@dataclass
class CriteriaScore:
    name: str = ""
    passed: bool = True
    score: float = 10.0
    feedback: str = ""


@dataclass
class CritiqueResult:
    status: str = "passed"  # "passed" or "needs_revision"
    overall_score: float = 10.0
    issues: List[str] = field(default_factory=list)
    required_changes: List[str] = field(default_factory=list)
    criteria_scores: Dict[str, CriteriaScore] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CritiqueResult":
        criteria = {}
        for k, v in data.get("criteria_scores", {}).items():
            if isinstance(v, dict):
                criteria[k] = CriteriaScore(
                    name=v.get("name", k),
                    passed=v.get("passed", True),
                    score=float(v.get("score", 10.0)),
                    feedback=v.get("feedback", ""),
                )
            elif isinstance(v, CriteriaScore):
                criteria[k] = v

        return cls(
            status=data.get("status", "passed"),
            overall_score=float(data.get("overall_score", 10.0)),
            issues=data.get("issues", []),
            required_changes=data.get("required_changes", []),
            criteria_scores=criteria,
        )

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["criteria_scores"] = {k: asdict(v) for k, v in self.criteria_scores.items()}
        return res
