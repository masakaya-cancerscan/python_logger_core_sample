# python-logger-core-sample

# Run cli
```
export PYTHONPATH="/{path}/python_logger_core_sample:$PYTHONPATH"
python sample/cs_logger.py
```

# Output Sample

## console log
```
/home/user/repo/python_logger_core_sample/.venv/bin/python /home/user/repo/python_logger_core_sample/sample/cs_logger.py 
[2022-09-07 09:11:51,724][DEBUG   ][/home/user/repo/python_logger_core_sample/sample/cslog.py:11] debug message
[2022-09-07 09:11:51,725][INFO    ][/home/user/repo/python_logger_core_sample/sample/cslog.py:12] info message
[2022-09-07 09:11:51,726][WARNING ][/home/user/repo/python_logger_core_sample/sample/cslog.py:13] warn message
[2022-09-07 09:11:51,726][ERROR   ][/home/user/repo/python_logger_core_sample/sample/cslog.py:14] error message
[2022-09-07 09:11:51,726][CRITICAL][/home/user/repo/python_logger_core_sample/sample/cslog.py:15] critical message
[2022-09-07 09:11:51,727][INFO    ][/home/user/repo/python_logger_core_sample/sample/cslog.py:21] custom value
[2022-09-07 09:11:51,727][ERROR   ][/home/user/repo/python_logger_core_sample/sample/cslog.py:26] division by zero
Traceback (most recent call last):
  File "/home/user/repo/python_logger_core_sample/sample/cs_logger.py", line 24, in <module>
    zero_division()
  File "/home/user/repo/python_logger_core_sample/sample/cs_logger.py", line 7, in zero_division
    1/0
ZeroDivisionError: division by zero
```
