# 使用 PowerShell 安装 Miniconda 教程

## 1. 下载与安装 Miniconda

在 PowerShell 中运行以下命令下载并静默安装 Miniconda：

```powershell
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S /InstallationType=JustMe /AddToPath=1 /RegisterPython=0" -Wait
del .\miniconda.exe

```

## 2. 初始化 PowerShell 环境

安装完成后，打开一个新的powershell窗口，运行以下命令初始化 PowerShell 环境，使 conda 命令可用：

```powershell
conda init powershell

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
