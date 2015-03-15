# -*- coding: utf-8 -*-
import os
from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PYB_PORT", 5000))
    host = os.environ.get("PYB_HOST", '127.0.0.1')

    app.run(host=host, port=port)
