import asyncio
import logging
from typing import Dict, Any
from .kafka.kafka_service import send_event
from .dapr_service import dapr_service

logger = logging.getLogger(__name__)

async def analyze_student_telemetry(user_id: str, event_data: Dict[str, Any]):
    """
    Analyzes student events in real-time to detect struggles.
    Implements the core Hackathon 'Struggle Detection' rule.
    """
    
    interaction_type = event_data.get("interaction_type")
    
    # Store telemetry in Dapr for persistence and pattern matching
    telemetry_key = f"telemetry_{user_id}"
    history = await dapr_service.get_state(telemetry_key) or []
    
    history.append({
        "type": interaction_type,
        "timestamp": event_data.get("timestamp"),
        "status": event_data.get("data", {}).get("execution_status")
    })
    
    # Limit history to last 10 events
    history = history[-10:]
    await dapr_service.save_state(telemetry_key, history)
    
    # Logic: Detect 3 consecutive code failures
    consecutive_failures = 0
    for event in reversed(history):
        if event.get("type") == "code_execution":
            if event.get("status") == "error":
                consecutive_failures += 1
            else:
                break # Success found, reset failure chain
                
    if consecutive_failures >= 3:
        logger.warning(f"🚨 STRUGGLE_ALERT: User {user_id} has {consecutive_failures} consecutive failures.")
        
        # Emit alert to Kafka for teacher dashboard
        alert_event = {
            "event_type": "STRUGGLE_ALERT",
            "user_id": user_id,
            "reason": "Consecutive code execution failures",
            "severity": "high",
            "timestamp": event_data.get("timestamp")
        }
        await send_event("teacher-alerts", alert_event, key=user_id)
        return True
    
    return False
