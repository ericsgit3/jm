name: Run jm.py manually (Selenium + Chrome)

on:
  workflow_dispatch: {}

jobs:
  run-jm:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      # 安装 Google Chrome + 运行浏览器常用依赖 + 虚拟显示器 Xvfb
      - name: Install Chrome & system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y --no-install-recommends \
            wget gnupg ca-certificates \
            xvfb \
            fonts-liberation \
            libnss3 libxss1 libasound2 \
            libgtk-3-0 libgbm1 \
            libu2f-udev \
            xdg-utils

          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
            | sudo gpg --dearmor -o /usr/share/keyrings/google-linux-keyring.gpg

          echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
            | sudo tee /etc/apt/sources.list.d/google-chrome.list

          sudo apt-get update
          sudo apt-get install -y --no-install-recommends google-chrome-stable

          google-chrome --version

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install selenium undetected-chromedriver requests

      # 如果你的 jm.py 本身会把浏览器设为 headless，这一步也能跑；
      # 即使没设 headless，xvfb-run 也能保证在 CI 环境里有显示器可用
      - name: Run jm.py (with Xvfb)
        run: |
          xvfb-run -a python jm.py
