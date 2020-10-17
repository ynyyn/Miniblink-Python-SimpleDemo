# Miniblink-Python-SimpleDemo
![license](https://img.shields.io/github/license/ynyyn/Miniblink-Python-SimpleDemo)
![platform](https://img.shields.io/badge/platform-Windows-007fe2)
![python](https://img.shields.io/badge/python-3.6%20|%203.7%20@%2032%20bit-blue)
![issues](https://img.shields.io/github/issues/ynyyn/Miniblink-Python-SimpleDemo)
![last-commit](https://img.shields.io/github/last-commit/ynyyn/Miniblink-Python-SimpleDemo)

A very simple Miniblink and Python 3 binding example via ctypes. Sketchy and rough prototype as it is, it might, someday in the future, become a not bad candidate to get a quick view of Miniblink.

#### Similar Project Recommendation

[lochen88/MBPython](https://github.com/lochen88/MBPython)

## What is Miniblink

[Miniblink](https://github.com/weolar/miniblink49) is a super lightweight web browser widget library, 
spiritual successor of [WKE](https://github.com/cexer/wke), 
specialized for developing HTML5 Web UI App (on Windows), whose kernel highly compactly integrated
[Chromium Blink](https://www.chromium.org/blink), [V8](https://v8.dev/), etc.

For more information, you may checkout Miniblink [Github page](https://github.com/weolar/miniblink49) 
and [official product website](https://miniblink.net/) (maybe Chinese only).

---

Belows are some notable things about Miniblink I would like to share in personal:

* Dynamic library, C-style API exported, concise and simple
* Ready to use as an HTML5 Web UI engine
* Kernel based on Chromium, BUT extremely lightweight
    * about 30 MB (32-bit) and 40 MB (64-bit), less than 10 MB after 7z compressed.
* **Only supports Windows platform currently**
    * from Windows XP to 10 and no need for any extra runtime.
* Open-source before but **CLOSE NOW** to be against annoying forks that violated open-source license
* **Provided with Free and Commercial solution, two sets of incompatible API**
    * This demo is for Miniblink Free solution.
    
Personal opinion: Miniblink vs CEF3 vs Electron

| Aspect      | Winner Order |
| ----------: | :------------ |
| Powerful    | CEF3 ≈ Electron >> **Miniblink** |
| Easy to Use | Electron >> **Miniblink** >> CEF3 |
| Lightweight | **Miniblink** >> CEF3 > Electron |
| Windows Compatibility | **Miniblink** >> CEF3 > Electron |
| Cross Platform | Electron >> CEF3, **Miniblink**: N/A, out |

\* Miniblink is referred to Miniblink Free solution.

## How to run this demo

### 1. Prepare

1. **Windows platform**, as the only platform that Miniblink supports at present.
2. Download a [Miniblink](https://github.com/weolar/miniblink49) pre-complied binary release if you haven't had a copy of that yet.  [Here (Miniblink releases)](https://github.com/weolar/miniblink49/releases), you may find Miniblink releases, the binary library is usually packed in compression with C header file and other useful resources.
3. Extract either all files or only `node.dll` (32-bit) and `miniblink_x64.dll` (64-bit) from the downloaded release compressed file and place them/it in the same folder of `main.py`.

### 2. Before Run: 32-bit or 64-bit?

The answer depends on what-bit (architecture) Python interpreter you are going to use to run this demo.

It must be clear that a dynamic library can only be loaded when it is of same-bit (architecture) as its host program, otherwise system will fail it. That means 32-bit process loads 32-bit library, 64-bit process loads 64-bit library, and no hybrid.

|                | 32-bit Miniblink | 64-bit Miniblink |
| -------------- | -------------- | -------------- |
| 32-bit Python | ✔              | ❌             |
| 64-bit Python | ❌             | ✔              |

`node.dll` is for 32-bit and `miniblink_x64.dll` is for 64-bit.
* If you are to use 64-bit, it is highly recommended to rename `miniblink_x64.dll` to `node.dll`.

### 3. Run

Run `main.py` via `python` or launcher `py`:

```powershell
py main.py    # or python main.py
```

or use `pyw` (or conventional `pythonw`) to run demo without console:

```powershell
pyw main.py    # or pythonw main.py
```

or use `py -3-32` or `py -3-64` to specify a 32-bit or 64-bit Python 3.


## Contents of Files and Directories in Demo

* `main_mini.py`: The minimal code to run Miniblink in Python.(And it's standalone, click-to-run with Python Standard Library!)
* `main.py`: (In progress) Added some fun stuff (events, etc.) based on `main_mini.py`.

* `official_demo_transcript`: (Coming soon) A Python transcript of the Miniblink official demo (origins from C++ demo_src).

## License

MIT License

## ...

I, actually a Python newbie... Sorry for any messy code or bad style, and, please feel free to point them out.
