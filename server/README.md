#deployment process:
pip install pyinstaller

pyinstaller --onefile manage.py

find the execute file at dist/manage
move manage to /home/app
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
Reload systemd: sudo systemctl daemon-reload
Start/Enable the service(s): 
sudo systemctl enable myapp-py.service
sudo systemctl start myapp-py.service 
sudo systemctl stop myapp-py.service 
sudo systemctl restart myapp-py.service
Check status: 
sudo systemctl status myapp-py.service
journalctl -u myapp-py.service -f
