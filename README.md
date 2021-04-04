# Webex Logging Handler

This is a simple Python logging handler that emits messages to Webex [incoming Webhooks](https://apphub.webex.com/messaging/applications/incoming-webhooks-cisco-systems-38054).

## Installing

To install run:

```bash
python -m pip install git+https://gitlab.systems.cll.cloud/jclarke/webex-log-handler.git
```

## Usage

First, obtain an incoming webhook URL from <https://apphub.webex.com/messaging/applications/incoming-webhooks-cisco-systems-38054>.

Here is a trivial usage.  But you'll likely want to use a `logger.conf` or the like.

```python
import logging
from webex_handler import WebexHandler

logger = logging.getLogger(__name__)
# The notice level is more severe than INFO but not as severe as WARNING.
logger.setLevel(WebexHandler.NOTICE)

wx = WebexHandler("https://webexapis.com/v1/webhooks/incoming/...")
wx.setLevel(WebexHandler.NOTICE)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
wx.setFormatter(formatter)

logger.addHandler(wx)
```

## Other Info

The WebexHandler uses markdown-formatted messages by default, but you can pass `use_markdown=False` to the WebexHandler constructor to use plain text.

Also, be cognizant than a high level (like INFO or DEBUG) can make things very chatty in Webex.  Consider a lower level to minimize noise.
