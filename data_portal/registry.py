from pony.orm import *
import json
import os

try:  
   username = os.environ.get("DB_USER")
   password = os.environ.get("DB_PASSWORD")
except KeyError: 
   print("Not exist environment value for %s" % "key_maybe_not_exist")

print("{},{}".format(username,password))

db = Database()
db.bind(provider='mysql', host='127.0.0.1',port=3306, user=username, passwd=password, db='IOT_HOTEL')

#Create tables
class User(db.Entity):
    username = PrimaryKey(str,auto=False)
    password_hash = Required(str)
    salt =  Required(str)
    devices = Set('Device')

class Device(db.Entity):
    mac = PrimaryKey(str,auto=False)
    device_type = Required(str)
    collector_version = Required(str)
    room = Required(str)
    owner = Required(User) 
    logs = Set('Log')

class Log(db.Entity):
    device = Required(Device)
    log_dump = Required(str)
    timestamp = Required(str)

#TODO OAuth
@db_session
def create_new_user(username,hash,salt):
    users =  select(user for user in User if user.username == username)
    if len(users) > 0:
        print("Invalid Username exists already")
    else:
        user = User(username=username,salt=salt,password_hash=hash)
        commit()
        return 'User has been added',200

@db_session
def create_new_log(log_dump,timestamp,device):
    log = Log(log_dump = log_dump,timestamp=timestamp,device=device)
    commit()
    return 'Log created',200

@db_session
def create_new_device(mac,device_type,collector_version,room,owner):
    if Device[mac] is not None:
        print("Device already registered")
    else:
        Device(mac=mac,device_type=device_type,collector_version=collector_version,room=room,owner=owner)   
        return '',200

@db_session
def return_user(user):
    return User[user].to_dict()

@db_session
def return_devices_for_user(owner_id,device_id=None):
    if device_id is None:
        device_list = []
        devices = User[owner_id].devices
        for device in devices:
            device_list.append(device.to_dict())
        return device_list
    else:
        device = Device[device_id] if Device[device_id].owner.username == owner_id else None
        return device

@db_session
def return_logs_for_device(owner_id,device_id,log_id=None):
    if log_id is None:
        log_list = []
        logs = select(log 
                        for owner in User
                        for device in owner.devices
                        for log in device.logs 
                        if (owner.username == owner_id and
                            device.mac == device_id ))
        for log in logs:
            log_list.append(log.to_dict())
        return log_list
    else:
        log = Log[log_id] if Log[log_id].device.mac == device_id and Log[log_id].device.owner.username == owner_id else None
        return log.to_dict()

db.generate_mapping(create_tables=True)


create_new_user("mike","pass","hash")
create_new_device("543f34fg34","Rasberry Pi","0.0.1","Kitchen","mike")
create_new_log("34,346,346,32,135,2345,35","5 am","543f34fg34")
