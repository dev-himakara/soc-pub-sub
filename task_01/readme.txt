Open two separate terminals and run:

Terminal 1 (Server):

```bash
cd ~/Desktop/SOC_assignment/soc-pub-sub/task_01
python3 server.py 5000
```
Terminal 2 (Client):

```bash
cd ~/Desktop/SOC_assignment/soc-pub-sub/task_01
python3 client.py 127.0.0.1 5000
Then type messages in the client terminal — they'll appear on the server terminal. Type terminate to cleanly disconnect.
```
