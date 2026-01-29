"""
Progress Agent for LearnFlow
Tracks and analyzes student progress
"""

import asyncio
import datetime
from typing import Dict, Any, List
from collections import defaultdict
import json

class ProgressAgent:
    def __init__(self):
        self.name = "Progress Agent"
        self.description = "Tracks and analyzes student progress"

        # In-memory storage (would be replaced with database in production)
        self.student_progress = defaultdict(lambda: defaultdict(dict))
        self.lesson_completion = defaultdict(list)
        self.difficulty_tracking = defaultdict(lambda: defaultdict(int))

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process progress-related requests"""
        if context and "student_id" in context:
            student_id = context["student_id"]

            # Get student progress
            student_progress = await self.get_student_progress(student_id)

            response = {
                "agent": "progress",
                "student_id": student_id,
                "progress_summary": student_progress,
                "recommendations": await self.get_recommendations(student_id),
                "message": f"Progress report for student {student_id}",
                "confidence": 0.9
            }

            return response
        else:
            return {
                "agent": "progress",
                "message": "Student ID required to retrieve progress information",
                "confidence": 0.8
            }

    async def update_progress(self, user_input: str, result: Dict[str, Any], context: Dict[str, Any] = None):
        """Update student progress based on their activity"""
        if not context or "student_id" not in context:
            return

        student_id = context["student_id"]
        timestamp = datetime.datetime.now().isoformat()

        # Determine activity type from result
        activity_type = result.get("agent", "unknown")
        activity_details = {
            "timestamp": timestamp,
            "activity_type": activity_type,
            "result": result,
            "input": user_input
        }

        # Store activity
        self.student_progress[student_id]["activities"].append(activity_details)

        # Update statistics
        self.student_progress[student_id]["last_activity"] = timestamp
        self.student_progress[student_id]["total_activities"] = len(self.student_progress[student_id]["activities"])

        # If this was a successful exercise completion
        if activity_type == "exercise" and result.get("type") == "solution_evaluation":
            score = result.get("evaluation", {}).get("score", 0)
            is_correct = result.get("evaluation", {}).get("is_correct", False)

            if is_correct:
                self.student_progress[student_id]["completed_exercises"] = \
                    self.student_progress[student_id].get("completed_exercises", 0) + 1
                self.student_progress[student_id]["exercise_score"] = \
                    self.student_progress[student_id].get("exercise_score", 0) + score

    async def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive progress report for a student"""
        progress = self.student_progress[student_id]

        if not progress:
            return {
                "student_id": student_id,
                "message": "No progress data available yet",
                "total_activities": 0,
                "completed_exercises": 0,
                "overall_score": 0,
                "engagement_level": "new",
                "last_activity": None
            }

        total_activities = progress.get("total_activities", 0)
        completed_exercises = progress.get("completed_exercises", 0)
        exercise_score = progress.get("exercise_score", 0)
        avg_exercise_score = exercise_score / completed_exercises if completed_exercises > 0 else 0

        # Determine engagement level
        engagement_level = "low"
        if total_activities > 20:
            engagement_level = "high"
        elif total_activities > 5:
            engagement_level = "medium"

        return {
            "student_id": student_id,
            "total_activities": total_activities,
            "completed_exercises": completed_exercises,
            "overall_score": avg_exercise_score,
            "engagement_level": engagement_level,
            "last_activity": progress.get("last_activity"),
            "recent_activities": progress["activities"][-5:] if "activities" in progress else [],
            "progress_percentage": min((completed_exercises * 10) if completed_exercises < 10 else 100, 100)
        }

    async def get_recommendations(self, student_id: str) -> List[Dict[str, Any]]:
        """Get personalized learning recommendations for a student"""
        progress = self.student_progress[student_id]
        recommendations = []

        if not progress:
            # New student - recommend starting with basics
            recommendations.append({
                "type": "curriculum",
                "priority": "high",
                "title": "Start with Basics",
                "description": "Begin with fundamental Python concepts",
                "suggested_exercises": ["Print Statement", "Variable Assignment"]
            })
        else:
            completed_exercises = progress.get("completed_exercises", 0)
            avg_score = progress.get("exercise_score", 0) / completed_exercises if completed_exercises > 0 else 0

            # If average score is low, recommend more practice on current level
            if avg_score < 60:
                recommendations.append({
                    "type": "practice",
                    "priority": "high",
                    "title": "More Practice Needed",
                    "description": "Focus on strengthening fundamentals before advancing",
                    "suggested_exercises": ["Even or Odd", "Sum of Numbers"]
                })
            elif avg_score < 80:
                recommendations.append({
                    "type": "advance",
                    "priority": "medium",
                    "title": "Ready for Next Level",
                    "description": "You're ready to tackle more challenging exercises",
                    "suggested_exercises": ["Simple Function"]
                })
            else:
                recommendations.append({
                    "type": "challenge",
                    "priority": "high",
                    "title": "Advanced Exercises",
                    "description": "Try more complex problems to continue growing",
                    "suggested_exercises": ["Advanced Function Problems"]
                })

            # Check for gaps in learning
            if completed_exercises < 3:
                recommendations.append({
                    "type": "completion",
                    "priority": "high",
                    "title": "Complete Foundational Exercises",
                    "description": "Finish the basic exercises to build a strong foundation",
                    "suggested_exercises": ["Print Statement", "Variable Assignment", "Even or Odd"]
                })

        return recommendations

    async def detect_struggles(self, student_id: str) -> List[Dict[str, Any]]:
        """Detect if a student is struggling with specific concepts"""
        progress = self.student_progress[student_id]
        struggles = []

        if not progress:
            return struggles

        activities = progress.get("activities", [])

        # Check for repeated low scores
        recent_evaluations = [
            act for act in activities
            if act.get("result", {}).get("agent") == "exercise"
            and act.get("result", {}).get("type") == "solution_evaluation"
        ][-5:]  # Last 5 evaluations

        if len(recent_evaluations) >= 3:
            low_scores = [
                eval_act for eval_act in recent_evaluations
                if eval_act.get("result", {}).get("evaluation", {}).get("score", 0) < 50
            ]

            if len(low_scores) >= 2:
                struggles.append({
                    "type": "repeated_failure",
                    "severity": "high",
                    "description": "Multiple recent low-scoring exercise submissions",
                    "recommended_action": "Review fundamental concepts or seek additional help"
                })

        # Check for lack of progress
        if len(activities) > 5 and progress.get("completed_exercises", 0) < 2:
            struggles.append({
                "type": "slow_progress",
                "severity": "medium",
                "description": "Slow progress in completing exercises",
                "recommended_action": "Focus on completing more exercises to build momentum"
            })

        return struggles

    async def generate_report(self, student_id: str) -> Dict[str, Any]:
        """Generate a comprehensive progress report"""
        progress = await self.get_student_progress(student_id)
        recommendations = await self.get_recommendations(student_id)
        struggles = await self.detect_struggles(student_id)

        return {
            "student_id": student_id,
            "generated_at": datetime.datetime.now().isoformat(),
            "summary": progress,
            "recommendations": recommendations,
            "struggles": struggles,
            "action_items": [rec for rec in recommendations if rec["priority"] in ["high", "medium"]]
        }

    def reset_student_progress(self, student_id: str):
        """Reset progress for a specific student"""
        if student_id in self.student_progress:
            del self.student_progress[student_id]