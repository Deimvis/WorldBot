from src.apps.core.state import GLOBAL_STATE


def get_subscription_builder(chat_id: int):
    return GLOBAL_STATE['quotes_subscription_builders'][chat_id]
