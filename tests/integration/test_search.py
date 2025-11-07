from unipile_sdk.client import Client
from unipile_sdk.models import CommonSearchParameter, LinkedinSearchPayload


def test_search(comm_client: Client):
    res = comm_client.ln_search.search(
        payload=LinkedinSearchPayload(api="classic", category="people"),
        limit=3,
    )
    assert len(res.items) == 3


def test_search_param(comm_client: Client, search_keyword: str):
    param = comm_client.ln_search.search_param(
        type=CommonSearchParameter.COMPANY, keywords=search_keyword
    )
    company = next(iter(param.items))
    assert company.id == "1035"


def test_retrieve_company(comm_client: Client, search_keyword: str):
    company = comm_client.ln_search.retrieve_company(identifier=search_keyword)
    assert company.id == "1035"


def test_retrieve_company_id(comm_client: Client, search_keyword: str):
    company_id = comm_client.ln_search.retrieve_company_id(
        url_or_name=search_keyword
    )
    assert company_id == "1035"
