import pytest
from unipile_sdk.client import Client

from unipile_sdk.helpers import iterate_paginated_api


def test_chat_attendees(comm_client: Client):
    attendees = comm_client.messages.chat_attendees()
    assert attendees is not None


def test_messages(comm_client: Client):
    found_messages = 0
    for attende in iterate_paginated_api(
        comm_client.messages.chat_attendees, max_total=100
    ):
        attendee_chats = comm_client.messages.list_chats_by_attendee(
            attendee_id=attende.id,
        )
        for chat in attendee_chats.items:
            messages = comm_client.messages.messages(chat_id=chat.id)
            found_messages = len(messages.items)

        if found_messages:
            break

    assert found_messages > 0


@pytest.mark.activities
def test_send_message(user_urn_to_message, ln_sending_message, comm_client: Client):
    if user_urn_to_message is None:
        pytest.skip("No user URN provided for testing")

    attendee_chats = comm_client.messages.list_chats_by_attendee(
        attendee_id=user_urn_to_message,
    )
    if not attendee_chats.items:
        return

    chat = attendee_chats.items[0]

    message = comm_client.messages.send_message(
        chat_id=chat.id,
        text=ln_sending_message
    )

    assert message is not None

@pytest.mark.activities
def test_send_message_to_attendees(ln_sending_message, comm_client: Client):
    attendees = comm_client.messages.chat_attendees(limit=100)

    for attendee in attendees.items:
        attendee_chats = comm_client.messages.list_chats_by_attendee(
            attendee_id=attendee.provider_id,
        )
        if len(attendee_chats.items) == 1:
            message = comm_client.messages.send_message_to_attendees(
                attendees_ids=[attendee.provider_id],
                text=ln_sending_message
            )
            assert message is not None

    raise AssertionError("No suitable attendee found for sending message")
