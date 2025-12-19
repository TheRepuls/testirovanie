from locust import HttpUser, task
import json
class OpenBMCUser(HttpUser):
    wait_time = 2
    @task(3)
    def get_system_info(self):
        self.client.get("https://localhost:2443/redfish/v1/Systems/system", auth=("root", "0penBmc"), verify=False, name="инфа")

    @task(2)
    def get_power_state(self):
        self.client.get("https://localhost:2443/redfish/v1/Chassis/chassis", auth=("root", "0penBmc"), verify=False, name="power");
	
    @task(1)
    def get_service_root(self):
        self.client.get("https://localhost:2443/redfish/v1/", auth=("root", "0penBmc"), verify=False, name="права")

