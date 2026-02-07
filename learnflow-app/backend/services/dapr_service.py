"""
Dapr Service for LearnFlow
Handles state management and service invocation via Dapr
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from dapr.clients import DaprClient

logger = logging.getLogger(__name__)

class DaprService:
    def __init__(self, store_name: str = "statestore"):
        self.store_name = store_name
        self.client = None

    def get_client(self) -> DaprClient:
        if self.client is None:
            self.client = DaprClient()
        return self.client

    async def save_state(self, key: str, value: Any):
        """Save state to Dapr state store"""
        try:
            with DaprClient() as client:
                client.save_state(
                    store_name=self.store_name,
                    key=key,
                    value=json.dumps(value)
                )
            logger.info(f"Saved state for key: {key}")
        except Exception as e:
            logger.error(f"Error saving state to Dapr: {str(e)}")

    async def get_state(self, key: str) -> Optional[Any]:
        """Get state from Dapr state store"""
        try:
            with DaprClient() as client:
                result = client.get_state(
                    store_name=self.store_name,
                    key=key
                )
                if result.data:
                    return json.loads(result.data)
            return None
        except Exception as e:
            logger.error(f"Error getting state from Dapr: {str(e)}")
            return None

    async def delete_state(self, key: str):
        """Delete state from Dapr state store"""
        try:
            with DaprClient() as client:
                client.delete_state(
                    store_name=self.store_name,
                    key=key
                )
            logger.info(f"Deleted state for key: {key}")
        except Exception as e:
            logger.error(f"Error deleting state from Dapr: {str(e)}")

    async def invoke_service(self, target_id: str, method_name: str, data: Any) -> Any:
        """Invoke another service via Dapr"""
        try:
            with DaprClient() as client:
                resp = client.invoke_method(
                    target_id,
                    method_name,
                    data=json.dumps(data)
                )
                return json.loads(resp.data)
        except Exception as e:
            logger.error(f"Error invoking service {target_id} via Dapr: {str(e)}")
            return None

dapr_service = DaprService()
