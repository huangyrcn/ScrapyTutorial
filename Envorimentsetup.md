# 使用 PowerShell 安装 Miniconda 教程

## 0. 启动脚本执行功能

在运行脚本之前，需要确保 PowerShell 允许执行脚本。请以管理员身份运行 PowerShell。可以通过以下命令设置脚本执行策略为 `RemoteSigned`，以允许本地脚本运行，同时要求远程脚本必须经过签名：

```powershell
set-executionpolicy remotesigned
```

## 1. 下载与安装 Miniconda

在 PowerShell 中运行以下命令下载并静默安装 Miniconda：

```powershell
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait .\miniconda.exe /S /InstallationType=JustMe /AddToPath=1 /RegisterPython=0
del .\miniconda.exe

```

## 2. 初始化 PowerShell 环境

安装完成后，打开一个新的powershell窗口，运行以下命令初始化 PowerShell 环境，使 conda 命令可用：

```powershell
conda init
```

重启 PowerShell 后，初始化设置生效。

## 3. 禁用自动激活 base 环境

若不希望每次启动 PowerShell 时自动激活 base 环境，可执行以下命令：

```powershell
conda config --set auto_activate_base false
```

后面需要使用时可以使用下面命令激活 conda 的默认环境

```powershell
conda activate 
```
