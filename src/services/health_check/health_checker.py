import time
import httpx

from entities.service_url_list_type import Service_Url_List_Type


class HealthCheck:

    def __init__(self, ctx):
        self.ctx = ctx

    def run_health_check(self):
        while True:
            self.run_health_checker()
            time.sleep(60)

    def run_health_checker(self):
        server_maps = [self.ctx.get(Service_Url_List_Type.All_Service_Urls.name)]
        success_status_code = (200, 204)

        for server_map in server_maps:
            for service, service_urls in server_map.data.items():
                for service_url in service_urls:
                    try:
                        response = httpx.get(service_url + service + "/ping")
                        if response.status_code not in success_status_code:
                            self.ctx.get("UrlService").unhealthy_service_url(service, service_url)
                    except Exception as ex:
                        print(ex)
                        self.ctx.get("UrlService").unhealthy_service_url(service, service_url)
                    else:
                        print("No Exception")
                        print("Service is healthy")
