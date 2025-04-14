#deployment process:
pip install pyinstaller

ssh app@13.250.6.53
cd /home/app/Desktop/Pathfinder-Analysis/server
rm -r dist
pyinstaller --onefile manage.py
cp /home/app/Desktop/Pathfinder-Analysis/server/dist/manage /home/app
use local terminal to cp the data into server node:
 scp app@13.250.6.53:/home/app/Desktop/Pathfinder-Analysis/server/dist/manage . 
 scp app@13.250.6.53:/home/app/Desktop/timing/timing.csv .
 scp manage app@api.fundureka.com:/home/app
 scp timing.csv app@api.fundureka.com:/home/app/Desktop/timing
now go to the server node to do the following step:
ssh app@api.fundureka.com
## how to deploy at server
sudo vi /etc/systemd/system/myapp-py.service
-------
[Unit]
Description=My Python Application
After=syslog.target
[Service]
User=app
ExecStart=/home/app/manage runserver_path --file_path=/home/app/Desktop/output_china/ --rank_file_path=/home/app/Desktop/output_search/ --comment_file_path=/home/app/Desktop/output_china/ --noreload
Restart=on-failure

[Install]
WantedBy=multi-user.target
-------
restart the server:
sudo systemctl stop myapp-py.service 
### if it has warming for deamon-reload run this command: 
sudo systemctl daemon-reload 
sudo systemctl start myapp-py.service 

------- command for testing.
Reload systemd: sudo systemctl daemon-reload
Start/Enable the service(s): 
sudo systemctl enable myapp-py.service
sudo systemctl start myapp-py.service 
sudo systemctl stop myapp-py.service 
sudo systemctl restart myapp-py.service
Check status: 
sudo systemctl status myapp-py.service
journalctl -u myapp-py.service -f
