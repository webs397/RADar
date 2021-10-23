# Instructions

1. create an instace of the Alarm class  
- the default frequency is 40 Hz
- the default values per second is 10
    - the measurements per value are calculated with:  (1/values_per_second)/(1/frequency)
2. in a while loop call the *fill_buffer* method of the Alarm class with the desired frequencie  
- Example:  
```
frequenz = 40
myalarm = Alarm(frequency=frequenz)
    while True:
        alarm = myalarm.compute_measurments()   # either True or Falses
        time.sleep(1/frequenz)
```

# TODO
make something with the alarm. Right now it triggers as soon as there is an acceleration of at least 3.5 m/s^2 on the y-axis. Thats it.  
There must be more to it ...