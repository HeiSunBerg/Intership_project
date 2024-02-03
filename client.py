import pyModbusTCP
from pyModbusTCP.client import ModbusClient
# import meter_list

conV = '192.168.1.114'
id = 1
modbusAddr = {
        'sensor': 'lovato DMED111',
        'modbus': {
            'energy': {
                'function': 'read_holding_registers',
                'addr': 6687,
                'words': 2,
                'divide': 1000,
                'format': {
                    'ieee': False
                }
            }
        }
    }


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


ModbusBMS = ModbusClient(host=conV, port=502, unit_id=id, auto_open=True, auto_close=True)
data = _modbusUtils(ModbusBMS, modbusAddr['modbus'])

print('ip:' + conV + ' || ' + 'meter_id:' + str(id) + ' || '
      + 'meter model:' + str(modbusAddr['sensor']) + ' || '
      + 'energy{kWh}:' + str(data))
