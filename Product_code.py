from pyModbusTCP.client import ModbusClient
import meter_list
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
import pyModbusTCP

scheduler = BlockingScheduler(({'apscheduler.timezone': 'Asia/Bangkok'}))


def _modbusUtils(ModbusBMS, modbus):
    addr = modbus['energy']['addr']
    divide = modbus['energy']['divide']
    function = modbus['energy']['function']
    ieee = modbus['energy']['format']['ieee']
    try:
        if function == 'read_holding_registers':
            val_list = ModbusBMS.read_holding_registers(addr, 2)
        if function == 'read_input_registers':
            val_list = ModbusBMS.read_input_registers(addr, 2)

        data = pyModbusTCP.utils.word_list_to_long(val_list=val_list, big_endian=True, long_long=False)[0]
        if ieee:
            data = pyModbusTCP.utils.decode_ieee(int(data), double=False)
        return data / divide
    except:
        return None


if __name__ == '__main__':

    @scheduler.scheduled_job("cron", minute="00,15,30,45")
    def insertDB():
        CONNECTION = "postgres://adminXten:xten1234@localhost:5432/td"
        conn = psycopg2.connect(CONNECTION)
        cursor = conn.cursor()
        temp = []
        # loop ip
        for conV in meter_list.conv:
            # loop id
            for sensor in conV['sensor']:
                # loop meter in conv
                for meter in conV['sensor'][sensor]:
                    ModbusBMS = ModbusClient(host=conV['ip'], port=502, unit_id=meter['id'], auto_open=True,
                                             auto_close=True)
                    # loop addr
                    for modbusAddr in meter_list.modbus_addr:
                        # check meter model
                        if modbusAddr['sensor'] == sensor:
                            data = _modbusUtils(ModbusBMS, modbusAddr['modbus'])
                            if data is not None:
                                SQL = "INSERT INTO meter (sensor_id, conv_ip, time, data) VALUES (%s, %s, date_trunc('minute', now()::timestamp with time zone), %s);"
                                value = (meter['id'], conV['ip'], data)
                                cursor.execute(SQL, value)
                                conn.commit()
        cursor.close()


    scheduler.start()