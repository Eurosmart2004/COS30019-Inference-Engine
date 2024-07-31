# COS30019 Assignment 2 - Inference Engine for Propositional Logic

## Description

This project is an inference engine developed for the Assignment 2 of course unit COS30019 - Introduction to Artificial Intelligence. It uses various logical inference methods to derive conclusions from a given knowledge base.

### General Information

- Programming Language: Python 3.10 or higher
- The program is designed to be executed with a CLI (e.g. Powershell for Windows).

## Installation

Before running the program, ensure that you have Python installed on your system. Then, follow these steps to set up a virtual environment and install the necessary packages:

1. Create a virtual environment:

```
python -m venv venv
```

2. Activate the virtual environment:

- On Windows:

```
.\venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

## Running the Program

To run the program, use the following command:

```
iengine <method> <filename>
```

Replace `<method>` with one of the following options based on the technique you want to use:

- `TT` for Truth Table checking
- `FC` for Forward Chaining
- `BC` for Backward Chaining
- `RES` for Resolution
- `DPLL` for Davis-Putnam-Logemann-Loveland

For example, to use Forward Chaining on a file named `test.txt`, the command would be:

```
iengine FC test.txt
```

Please place all the `.txt` files in a folder named `data`. Each file should follow this structure:

```
TELL
... (Knowledge base, each fact or rule separated by a semicolon)
ASK
... (Query)
EXPECTED (Optional)
... (Expected result to verify the algorithm)
```

For example, a file might look like this:

```
TELL
a=>b; a;
ASK
b
EXPECTED
YES
```

In this example, `a=>b; a;` is the knowledge base, `b` is the query, and `YES` is the expected result.

## Contributing

This project is a collaborative effort between Quang Thien and Thanh Minh. We both have contributed significantly to the development and success of this project.

## License

This project is licensed under the MIT License.
