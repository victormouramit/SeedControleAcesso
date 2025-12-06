from pyintelbras import IntelbrasAPI
import time

# Verificar número de alarmes
# action='getConfig', name='AlarmOut'
# Definir um alarme como ligado ou desligado
# action="setConfig&AlarmOut[1].Mode=1", name="AlarmOut"
# Verificar alarme ligado ou desligado

class Camera:
    def __init__(self,ip,passwd,login="admin"):
        self.login = login
        self.passwd = passwd
        self.ip = ip
        self.intelbras = IntelbrasAPI(f"http://{self.ip}")
        self.intelbras.login(login,passwd)
    def pulsate(self,number_alarm_out = 1,secs=.5):
        self.intelbras.configManager(action=f"setConfig&AlarmOut[{number_alarm_out}].Mode=1", name="AlarmOut")
        time.sleep(secs)
        self.intelbras.configManager(action=f"setConfig&AlarmOut[{number_alarm_out}].Mode=0", name="AlarmOut")
    def getOutputAlarms(self):
        return self.intelbras.configManager(action="getConfig",name="AlarmOut").text



#c = Camera("192.168.40.3","Ct14!#6tVq@")
#alarms = c.pulsate()