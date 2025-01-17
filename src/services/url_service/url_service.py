from src.entities.service_url_list_type import Service_Url_List_Type


class UrlService:

    def __init__(self, ctx):
        self.ctx = ctx

    def ping(self):
        return {"message": "pong"}

    def get_all_servers(self, service):
        return self.ctx.get(Service_Url_List_Type.All_Service_Urls.name).get(service)

    # These are servers that have been deregistered.
    def get_deregistered_servers(self, service):
        return self.ctx.get(Service_Url_List_Type.Deregistered_Service_Urls.name).get(service)

    # These are servers that are not healthy.
    def get_unhealthy_servers(self, service):
        return self.ctx.get(Service_Url_List_Type.Unhealthy_Service_Urls.name).get(service)

    # When an url is registered it is added to the "Service_Urls"
    def register_service_url(self, service: str, service_url: str):
        self._add_server_to_url_list_by_type(service, service_url, Service_Url_List_Type.All_Service_Urls)
        return {"message": "Service URL registered successfully"}

    # When an url is deregistered it is added to the "Deregistered_Service_Urls"
    # If the url exists in the "Unhealthy_Service_Urls", it is removed from it
    def deregister_service_url(self, service: str, service_url: str):
        self._add_server_to_url_list_by_type(service, service_url, Service_Url_List_Type.Deregistered_Service_Urls)
        self._remove_server_from_list_by_type(service, service_url, Service_Url_List_Type.Unhealthy_Service_Urls)
        return {"message": "Service URL de-registered successfully"}

    # When an url is unhealthy it is added to the Unhealthy_Service_Urls
    def unhealthy_service_url(self, service: str, service_url: str):
        self._add_server_to_url_list_by_type(service, service_url, Service_Url_List_Type.Unhealthy_Service_Urls)
        return {"message": "Service URL marked unhealthy successfully"}

    def get_service_url(self, service):
        all_service_urls = self.ctx.get(Service_Url_List_Type.All_Service_Urls.name).get(service)
        deregistered_service_urls = self.ctx.get(Service_Url_List_Type.Deregistered_Service_Urls.name).get(service)
        unhealthy_service_urls = self.ctx.get(Service_Url_List_Type.Unhealthy_Service_Urls.name).get(service)

        # we do the modulo here on the given list as it is possible the list is shorter than the current index
        # modulo by list len -> i + 1 % len(servers)
        inactive_servers = set()
        if deregistered_service_urls:
            inactive_servers = inactive_servers.union(set(deregistered_service_urls))
        if unhealthy_service_urls:
            inactive_servers = inactive_servers.union(set(unhealthy_service_urls))

        server_index_to_return = self.ctx.get("Server_Index").get(service) % len(all_service_urls)
        initial_index = server_index_to_return

        while all_service_urls[server_index_to_return] in inactive_servers:
            server_index_to_return = (server_index_to_return + 1) % len(all_service_urls)
            if server_index_to_return == initial_index:
                # No healthy server found after a complete round
                raise Exception("No healthy service URL available")

        # storing the next possible index
        self.ctx.get("Server_Index").set(service, server_index_to_return + 1)
        return all_service_urls[server_index_to_return]

    def _add_server_to_url_list_by_type(self, service: str, service_url: str, list_type: Service_Url_List_Type):
        service_urls = self.ctx.get(list_type.name).get(service)
        if service_urls:
            if service_url not in set(service_urls):
                service_urls.append(service_url)
        else:
            service_urls = [service_url]
            if list_type == Service_Url_List_Type.All_Service_Urls:
                self.ctx.get("Server_Index").set(service, 0)

        self.ctx.get(list_type.name).set(service, service_urls)

    def _remove_server_from_list_by_type(self, service: str, service_url: str, list_type: Service_Url_List_Type):
        service_urls = self.ctx.get(list_type.name).get(service)
        if service_urls:
            if service_url in set(service_urls):
                service_urls.remove(service_url)
        else:
            if list_type == Service_Url_List_Type.All_Service_Urls:
                self.ctx.get("Server_Index").remove(service)

        self.ctx.get(list_type.name).set(service, service_urls)


