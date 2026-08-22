# Windows Installation and Setup

Prerequisites:
- Windows 10/11 with virtualization enabled in BIOS
- VirtualBox (6.x/7.x)
- Vagrant
- Git
- Python 3.8+ and pip

Steps:

1. Install VirtualBox: https://www.virtualbox.org/
2. Install Vagrant: https://www.vagrantup.com/
3. Install Git: https://git-scm.com/
4. Install Python: https://www.python.org/

Clone the repository:

```powershell
git clone https://github.com/yourname/linux-learning-platform.git
cd linux-learning-platform
```

Install Python dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the prerequisite check:

```powershell
.\scripts\install.ps1
```

Start the backend API:

```powershell
.\scripts\run_backend.ps1
```

Open a new PowerShell and start the lab VM:

```powershell
.\scripts\start.ps1
```

Open the web UI at http://127.0.0.1:8000/static/index.html

Notes:
- If `vagrant up` fails, run `vagrant box add generic/rocky8` to pre-download the box.
- Use `vagrant ssh` to connect directly to the VM.
