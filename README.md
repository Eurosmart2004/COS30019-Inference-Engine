# COS30019 Assignment 2 - Inference Engine for Propositional Logic

## Description

This project is an inference engine developed for the Assignment 2 of course unit COS30019 - Introduction to Artificial Intelligence. It uses various logical inference methods to derive conclusions from a given knowledge base.

### General Information

* Programming Language: Python 3.12.3
* The program is designed to be executed with a CLI (e.g. Powershell for Windows).

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

You can run program following this method:

```
./iengine <method> <filename>
```

1. If you want to use Truth Table checking

```
./iengine TT <filename>
```

2. If you want to use Forward Chaining

```
./iengine FC <filename>
```

3. If you want to use Backward Chaining

```
./iengine BC <filename>
```

## Contributing

This project is a collaborative effort between Quang Thien and Minh. We both have contributed significantly to the development and success of this project.

## License

This project is licensed under the MIT License.
