import sys
from Registry import Registry
from rich import print

reg_SYSTEM = Registry.Registry(r"Path_To_SYSTEM")
time_zone_key = reg_SYSTEM.open(r"ControlSet001\Control\TimeZoneInformation") #Проверить точную временную зону
comp_name_key = reg_SYSTEM.open(r"ControlSet001\Control\ComputerName\ComputerName")
interface_key = reg_SYSTEM.open(r"ControlSet001\Services\Tcpip\Parameters\Interfaces")

reg_SOFTWARE = Registry.Registry(r"Path_To_SOFTWARE")
sys_info_key = reg_SOFTWARE.open(r"Microsoft\Windows NT\CurrentVersion")
softwares_key = reg_SOFTWARE.open(r"Microsoft\Windows\CurrentVersion\Uninstall")

reg_SAM = Registry.Registry(r"Path_To_SAM")
names_key = reg_SAM.open(r"SAM\Domains\Account\Users\Names")

print()
print("================= Время и имя: =================")
print()
print("Временная зона: ", time_zone_key["TimeZoneKeyName"].value())
print("Имя компьютера: ", comp_name_key["ComputerName"].value())
print()
print("================= Интерфейсы: =================")
print()
for subkey in interface_key.subkeys():
    print ("GUID интерфейса: ", subkey.name())

    def get_value(name):
        try:
            return subkey.value(name).value()
        except Registry.RegistryValueNotFoundException:
            return "<not set>"

    print(f"  DHCP IP: {get_value('DhcpIPAddress')}")
    print(f"  Subnet: {get_value('DhcpSubnetMask')}")
    print(f"  Gateway: {get_value('DhcpDefaultGateway')}")
    print(f"  DNS: {get_value('NameServer')}")
    print(f"  Domain: {get_value('Domain')}")
    print()
print("================= Информация о системе: =================")
print()
print("Версия ОС: ", sys_info_key.value("ProductName").value())
print("Path: ", sys_info_key.value("PathName").value())
print("Доп информация о системе: ", sys_info_key.value("EditionID").value())


print()
print("================= Установленное ПО: =================")
print()
for subkey in softwares_key.subkeys():
    def get_value(name):
        try:
            return subkey.value(name).value()
        except Registry.RegistryValueNotFoundException:
            return "<not set>"

    name = get_value('DisplayName')
    if name == "<not set>":
        continue

    print ("ПО: ", subkey.name())
    print("------------------------------------------")
    print(f"  Имя: {get_value('DisplayName')}")
    print(f"  Путь: {get_value('DisplayIcon')}")
    print(f"  Версия: {get_value('DisplayVersion')}")
    print("------------------------------------------")
    print()

print("================= Локальные пользователи: =================")

for subkey in names_key.subkeys():

    def get_value_type(name):
        try:
            return subkey.value(name).value_type()
        except Registry.RegistryValueNotFoundException:
            return "<not set>"
    print ("Пользователь: ", subkey.name(), f"RID: {get_value_type('(default)')}")
