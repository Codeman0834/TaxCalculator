# Tax Calculator

A simple command-line tax calculator with configurable brackets.

## Usage

```bash
python tax_calculator.py 85000 --status single
```

Override the standard deduction:

```bash
python tax_calculator.py 85000 --status married --standard-deduction 30000
```

Provide a custom bracket file (JSON):

```bash
python tax_calculator.py 85000 --brackets-file brackets.json
```

### Brackets file format

```json
{
  "standard_deductions": {
    "single": 13850,
    "married": 27700
  },
  "brackets": {
    "single": [
      {"threshold": 0, "rate": 0.10},
      {"threshold": 11000, "rate": 0.12}
    ],
    "married": [
      {"threshold": 0, "rate": 0.10},
      {"threshold": 22000, "rate": 0.12}
    ]
  }
}
```
