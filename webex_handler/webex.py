import logging
import requests
import time
import threading


class WebexHandler(logging.Handler):
    """
    A handler class which sends log messages to a Webex incoming webhook.
    """

    # Define a log level above INFO but below warning.
    NOTICE = logging.INFO + 5

    headers = {"Content-type": "application/json"}

    def __init__(self, webhook_url, use_markdown=True):
        """
        Initialize a handler.

        This requires a webhook URL and you can optionlly
        turn off markdown.
        """
        logging.Handler.__init__(self)

        self.url = webhook_url
        self.use_markdown = use_markdown

    def emit(self, record):
        """
        Emit a record.

        The record is formatted and then sent to Webex. If
        exception information is present, it is NOT sent to the server.
        """
        msg = self.format(record)

        payload = {}
        if self.use_markdown:
            payload["markdown"] = msg
        else:
            payload["text"] = msg

        thr = threading.Thread(target=self._send_msg, name="WebexMsgSender", kwargs={"payload": payload, "record": record})
        thr.start()

    def _send_msg(self, payload, record):
        while True:
            try:
                r = requests.post(self.url, headers=self.headers, json=payload)
                r.raise_for_status()
                break
            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    sleep_time = int(e.response.headers.get("retry-after"))
                    while sleep_time > 10:
                        time.sleep(10)
                        sleep_time -= 10

                    time.sleep(sleep_time)
                else:
                    self.handleError(record)
                    break
            except Exception:
                self.handleError(record)
                break
