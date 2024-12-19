# Jaculus Library Manager (JLM)

JLM is a simple library manager that helps you manage libraries in the Jaculus environment.

## Installation

**To install JLM globally, use pip:**

```bash
pip install git+https://github.com/C2Coder/Jaculus-library-manager.git
```

<br>

**or user install:**

```bash
pip install --user git+https://github.com/C2Coder/Jaculus-library-manager.git
```

<br>

**or pipx install: (tested)**

```bash
pipx install git+https://github.com/C2Coder/Jaculus-library-manager.git
```

<br>

## Usage

\* every function will create a `libs.json` file (if not present)

**List all avaliable commands**

```bash
jlm --help
```

<br>


**List all installed libraries**

```bash
jlm list
```
- lists all installed libraries

<br>


**List all avaliable libraries from server**

```bash
jlm avaliable
```
- lists all avaliable libraries from server

<br>


**Install a library**

```bash
jlm install <library name>
```
- installs a library from server

<br>

**Install libraries from file**

```bash
jlm install
```
- installs all libraries from `libs.json` file

<br>

**Install a library**

```bash
jlm update <library name>
```
- update a single installed library (from `libs.json` file)

<br>

**Install libraries from file**

```bash
jlm update
```
- update all installed libraries (from `libs.json` file)

<br>