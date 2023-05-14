import screens

rcrms_hub = screens.ScreenSession('RCRMS_HUB')
rcrms_survival = screens.ScreenSession('RCRMS_SURVIVAL')
rcrms_pvp = screens.ScreenSession('RCRMS_PvP')

rcrms_hub.send_command("cd /root/rcrms/RCRMS-HUB")
rcrms_hub.send_command("java -jar server.jar host RCR_HUB")

rcrms_survival.send_command("cd /root/rcrms/RCRMS-SURVIVAL")
rcrms_survival.send_command("java -jar server.jar host Domain")

rcrms_pvp.send_command("cd /root/rcrms/RCRMS-PvP")
rcrms_pvp.send_command("java -jar server.jar host The_real_king_of_the_territory pvp")