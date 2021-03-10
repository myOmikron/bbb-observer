# bbb-observer

A small script running on a bigbluebutton server to forward redis events.

---

It subscribes to the `from-akka-apps-redis-channel` channel on bigbluebutton's redisPUBSUB and listens for events.

Once it receives an event whose name matches the config, it will forward the event using a POST request to configurated url.

## Config

When the script is called for the first time, it generates an empty config file and quits.

It contains the following structure:

- **redis**: Where to find the redis server (shouldn't need to be changed)
  - **host** (default: localhost)
  - **port** (default: 6379)
  - **db** (default: 0)
- **url**: url to POST the event on
- **events**: list of event names to be forwarded
- **verify_ssl_certs**: turn of for self-signed certs (default: true)
