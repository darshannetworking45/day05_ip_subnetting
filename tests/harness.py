import contextlib
import importlib.util
import io
import os
import sys
from pathlib import Path

from netmiko.exceptions import NetmikoTimeoutException
from ntc_templates.parse import parse_output

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from common import netutils  
from sample_outputs import COMMANDS  

os.environ["NET_USERNAME"] = "test"
os.environ["NET_PASSWORD"] = "test"

UNREACHABLE = {"SW-ACCESS-02"}      
SENT = {}                           
FAILED = []
TEST_OUTPUT = ROOT / "output" / "_test"


class FakeConn:
    def __init__(self, dev):
        self.dev = dev
        SENT.setdefault(dev["hostname"], [])

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def send_command(self, cmd, use_textfsm=False, **kw):
        data = COMMANDS[cmd].replace("{host}", self.dev["hostname"]).replace("{serial}", "FOC1234ABCD")
        return parse_output(platform="cisco_ios", command=cmd, data=data) if use_textfsm else data

    def send_config_set(self, commands):
        SENT[self.dev["hostname"]].extend(commands)
        return ""

    def save_config(self):
        SENT[self.dev["hostname"]].append("<write memory>")


def fake_connect(device, creds, timeout=15):
    if device["hostname"] in UNREACHABLE:
        raise NetmikoTimeoutException("simulated timeout")
    return FakeConn(device)


netutils.connect = fake_connect
netutils.OUTPUT_DIR = TEST_OUTPUT


def run_script(rel_path, *args, patch=None):
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec) # type: ignore
    spec.loader.exec_module(module) # type: ignore
    for name, value in (patch or {}).items():
        setattr(module, name, value)
    old_argv, sys.argv = sys.argv, [path.name, *args]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            module.main()
    finally:
        sys.argv = old_argv
    return buf.getvalue()


def check(name, output, *must_contain):
    missing = [text for text in must_contain if text not in output]
    print(f"{'PASS' if not missing else 'FAIL'}  {name}")
    if missing:
        FAILED.append(name)
        print("      missing:", missing)
        print(output)
