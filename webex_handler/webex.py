import logging
import requests
import time


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
        try:
            msg = self.format(record)

            payload = {}
            if self.use_markdown:
                payload["markdown"] = msg
            else:
                payload["text"] = msg

            r = requests.post(self.url, headers=self.headers, json=payload)
            r.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                sleep_time = int(e.response.headers.get("retry-after"))
                while sleep_time > 10:
                    time.sleep(10)
                    sleep_time -= 10

                time.sleep(sleep_time)
            else:
                self.handleError(record)
        except Exception:
            self.handleError(record)
