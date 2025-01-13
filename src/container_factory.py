from src.services.url_service.url_service import UrlService
from src.resources.key_store.in_memory_key_store import InMemoryKeyStore

from src.container.container import container

from src.entities.service_url_list_type import Service_Url_List_Type


def create_container():
    container.set(Service_Url_List_Type.All_Service_Urls.name, InMemoryKeyStore())
    container.set(Service_Url_List_Type.Unhealthy_Service_Urls.name, InMemoryKeyStore())
    container.set(Service_Url_List_Type.Deregistered_Service_Urls.name, InMemoryKeyStore())
    container.set("Server_Index", InMemoryKeyStore())
    container.set("UrlService", UrlService(container))
    return container
