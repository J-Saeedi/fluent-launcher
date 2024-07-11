nuitka --standalone  --output-dir=build --no-deployment-flag=self-execution .\fluent-launcher.py
upx -9 .\build\fluent-launcher.dist\*
