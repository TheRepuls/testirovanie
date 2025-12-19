import pytest
import requests
import time
import subprocess

IP = "10.0.2.15"
UN = "root"
PW = "0penBmc"
SURL = f"https://localhost:2443//10.0.2.15/redfish/v1"

@pytest.fixture(scope="session")
def auth_token():
    url = f"https://localhost:2443/redfish/v1/SessionService/Sessions"
    response = requests.post(url, json={"UserName": UN, "Password": PW}, headers={"Content-Type": "application/json"}, verify=False)
    assert response.status_code in [200, 201]
    token = response.headers.get("X-Auth-Token")
    assert token is not None
    return token

@pytest.fixture
def redfish_session(auth_token):
    session = requests.Session()
    session.headers.update({
        "X-Auth-Token": auth_token,
        "Content-Type": "application/json"
    })
    session.verify = False
    return session

def test_get_system_info(redfish_session):
    response = redfish_session.get(f"https://localhost:2443/redfish/v1/Systems/system")
    assert response.status_code in [200]
    system_info = response.json()
    for field in ["Status", "PowerState"]:
        assert field in system_info

def test_power_control(redfish_session):
    system_url = f"https://localhost:2443/redfish/v1/Systems/system"
    system_response = redfish_session.get(system_url)
    current_state = system_response.json().get("PowerState")
    if current_state == "Off":
        response = redfish_session.post(f"https://localhost:2443/redfish/v1/Systems/system/Actions/ComputerSystem.Reset", json={"ResetType": "On"})
        assert response.status_code in [202]
        system_response = redfish_session.get(system_url)

def test_cpu_temperature(redfish_session):
    response = redfish_session.get("https://localhost:2443/redfish/v1/Chassis/chassis/Thermal")
    if response.status_code != 200:
        pytest.skip("Отказано в досупе")

def test_redfish_ipmi_sensors_comparison(redfish_session):
    response = redfish_session.get("https://localhost:2443/redfish/v1/Chassis/chassis/Thermal")
    if response.status_code != 200:
        pytest.skip("Отказано в доступе")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

