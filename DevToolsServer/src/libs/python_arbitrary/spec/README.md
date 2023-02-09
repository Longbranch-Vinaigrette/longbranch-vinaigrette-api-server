# Spec

The app must replace the following with its respective values:
$DEVTOOLS_ARGS: This SHALL be replaced by variables named in the following way:
DEVTOOLS_ARG_[n] = [VALUE]
Where [n] represents the number of the argument.
Where [VALUE] represents its corresponding value.
Example:
```python
DEVTOOLS_ARG_1 = "Some text"
DEVTOOLS_ARG_2 = { "username": "username", "password": "password" }
```

$USER_CODE: This MUST be replaced by the code given by the user.
Example:
```python
DEVTOOLS_ARG_1 = "Some text"
### --- Auto-generated code ends ---
print("Argument given: ", DEVTOOLS_ARG_1)
```

# Communication

The running script MUST retrieve the variable 'DEVTOOLS_RESULT' when available, which should
be the result the user expected.
