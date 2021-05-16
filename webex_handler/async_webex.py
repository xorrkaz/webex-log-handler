from aiolog import base
import aiohttp
import asyncio
import logging


class AsyncWebexHandler(base.Handler):
    """
    A handler class which sends log messages to a Webex incoming webhook.
    """

    # Define a log level above INFO but below warning.
    NOTICE = logging.INFO + 5

    headers = {"Content-type": "application/json"}

    def __init__(self, webhook_url, use_markdown=True, **kwargs):
        """
        Initialize a handler.

        This requires a webhook URL and you can optionlly
        turn off markdown.

        :param webhook_url: The URL for the incoming webhook (complete with token)
        :param use_markdown: Whether or not to use markdown or plain text for the message body
        """
        super().__init__(**kwargs)

        self.url = webhook_url
        self.use_markdown = use_markdown

    async def store(self, entries):
        """
        Queue a log message.

        The message is formatted and then sent to Webex.  Backoff is applied
        if rate-limiting is encountered.

        :param entries: List of strings to send
        """
        msg = "\n".join(entries)

        payload = {}
        if self.use_markdown:
            payload["markdown"] = msg
        else:
            payload["text"] = msg

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(self.url, headers=self.headers, json=payload) as resp:
                    if resp.status < 300:
                        break
                    elif resp.status == 429:
                        wait = int(resp.headers.get("retry-after"))
                        await asyncio.sleep(wait)
                    else:
                        break
