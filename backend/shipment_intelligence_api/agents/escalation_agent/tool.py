from langchain_core.tools import tool


@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """
    Send an email to a recipient.

    Use for detailed customer communication, status updates,
    and escalation notifications requiring full context.

    Args:
        recipient: Email address.
        subject: Short message title.
        body: Full message content.
    """
    # TODO: Integrate with email service provider
    return f"Email sent successfully to {recipient}"


@tool
def send_sms(message: str, phone_number: str) -> str:
    """
    Send an SMS message.

    Use for urgent or time-sensitive alerts that require
    immediate customer attention.

    Args:
        message: Short alert message.
        phone_number: Recipient phone number.
    """
    # TODO: Integrate with SMS service provider
    return f"SMS sent successfully to {phone_number}"


@tool
def create_support_ticket(
    shipment_id: str, issue: str, priority: str = "medium"
) -> str:
    """
    Create a support ticket for operational investigation
    and internal handling.

    Use when shipment issues require tracking,
    escalation, or resolution by operations teams.

    Args:
        shipment_id: Related shipment identifier.
        issue: Description of the problem.
        priority: low, medium, high, or critical.
    """
    # TODO: Integrate with support ticket management system
    return f"Support ticket created for shipment {shipment_id} with priority {priority}"
