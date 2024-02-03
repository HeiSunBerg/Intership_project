from pyModbusTCP.client import ModbusClient
import struct
import psycopg2 as p2

connection = p2.connect(
    host='localhost',
    database='postgres',
    user='postgres',
    password='admin1234',
    port=5432, )
connection.autocommit = True
cursor = connection.cursor()
create_table = """
                CREATE TABLE IF NOT EXISTS vol_meter(
                            id serial primary key,
                            voltage float,
                            at TIMESTAMP)
                """

cursor.execute(create_table)
# connection.close()

client = ModbusClient(host="192.168.1.232", unit_id=187,timeout=10, port=502, auto_open=True)

# Read two holding registers starting from address 1
registers = client.read_holding_registers(0, 2)

if registers is not None:
    # Combine the two 16-bit register values into a single 32-bit value
    # Switch the order of the registers for little endian
    raw = (registers[0] << 16) | registers[0]

    # Convert to float
    vol = struct.unpack('!f', struct.pack('!I', raw))[0]
    insert_table = '''
                INSERT INTO vol_meter(voltage,at)
                VALUES({},NOW());
                '''.format(vol)
    cursor.execute(insert_table)
    connection.close()
    print(vol)  # print the voltage value


else:
    print("Reading error")
