#!/bin/sh

TIME_ZONE=${TIME_ZONE:=UTC}
echo "timezone=${TIME_ZONE}"
cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
echo "${TIME_ZONE}" >/etc/timezone

echo "$(date) - start github project boards backup scheduler"
while :; do
    DATE=$(date +%Y%m%d-%H%M%S)

    for u in $(echo $GITHUB_USER | tr "," "\n"); do
        echo "$(date) - execute github project boards backup for ${u}, ${DATE}"
        python3 /srv/main.py --user=${u} --token=$TOKEN --output-directory=/srv/var/${DATE}/${u}
    done

    echo "$(date) - cleanup"

    ls -d1 /srv/var/* | head -n -${MAX_BACKUPS} | xargs rm -rf

    echo "$(date) - sleep for 1 day"
    sleep 1d
done