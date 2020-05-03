# Wireshark debug of BLE comms #
## Wireshark filter to single mac ##
bluetooth.src == 3c:a5:09:0a:85:79 || bluetooth.dst == 3c:a5:09:0a:85:79 (R Tablet)
bluetooth.src == a8:81:95:1e:25:43 || bluetooth.dst == a8:81:95:1e:25:43 (F Tablet)
R = BMS-initial
F = rasp-extradescriptors

```
R -> 789	Sent Read By Group Type Request, GATT Primary Service Declaration, Handles: 0x0001..0xffff
F -> 291	Sent Read By Group Type Request, GATT Primary Service Declaration, Handles: 0x0001..0xffff
		R 0210000b0007000400100100ffff0028
		F 0210000b0007000400100100ffff0028
			100100ffff0028
			Bluetooth Attribute Protocol
				Opcode: Read By Group Type Request (0x10)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..01 0000 = Method: Read By Group Type Request (0x10)
				Starting Handle: 0x0001
				Ending Handle: 0xffff
				UUID: GATT Primary Service Declaration (0x2800)

R <- 795	Rcvd Read By Group Type Response, Attribute List Length: 2, Generic Access Profile, Unknown
F <- 294	Rcvd Read By Group Type Response, Attribute List Length: 2, Generic Access Profile, Generic Attribute Profile
		R 02102012000e00040011060100070000180800ffffe0ff
		F 02102012000e0004001106010005000018060009000118
			R 11060100070000180800ffffe0ff
			F 1106010005000018060009000118
			Bluetooth Attribute Protocol
				Opcode: Read By Group Type Response (0x11)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..01 0001 = Method: Read By Group Type Response (0x11)
				Length: 6
				R Attribute Data, Handle: 0x0001, Group End Handle: 0x0007, UUID: Generic Access Profile
				F Attribute Data, Handle: 0x0001, Group End Handle: 0x0005, UUID: Generic Access Profile
					Handle: 0x0001 (Generic Access Profile)
						[UUID: Generic Access Profile (0x1800)]
					R Group End Handle: 0x0007
					F Group End Handle: 0x0005
					UUID: Generic Access Profile (0x1800)
				R Attribute Data, Handle: 0x0008, Group End Handle: 0xffff, UUID: Unknown
				F Attribute Data, Handle: 0x0006, Group End Handle: 0x0009, UUID: Generic Attribute Profile
					R Handle: 0x0008 (Unknown)
					F Handle: 0x0006 (Generic Attribute Profile)
						R [UUID: Unknown (0xffe0)]
						F [UUID: Generic Attribute Profile (0x1801)]
					R Group End Handle: 0xffff
					F Group End Handle: 0x0009
					R UUID: Unknown (0xffe0)
					F UUID: Generic Attribute Profile (0x1801)
				[UUID: GATT Primary Service Declaration (0x2800)]
				[Request in Frame: 789]

-> 796	Sent Read By Type Request, GATT Include Declaration, Handles: 0x0001..0x0007
		0210000b000700040008010007000228
			08010007000228
			Bluetooth Attribute Protocol
				Opcode: Read By Type Request (0x08)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..00 1000 = Method: Read By Type Request (0x08)
				Starting Handle: 0x0001
				Ending Handle: 0x0007
				UUID: GATT Include Declaration (0x2802)

<- 798	Rcvd Error Response - Attribute Not Found, Handle: 0x0001 (Generic Access Profile)
		021020090005000400010801000a
			010801000a
			Bluetooth Attribute Protocol
				Opcode: Error Response (0x01)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..00 0001 = Method: Error Response (0x01)
				Request Opcode in Error: Read By Type Request (0x08)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..00 1000 = Method: Read By Type Request (0x08)
				Handle in Error: 0x0001 (Generic Access Profile)
					[UUID: Generic Access Profile (0x1800)]
				Error Code: Attribute Not Found (0x0a)
				[UUID: GATT Include Declaration (0x2802)]

-> 799	Sent Read By Type Request, GATT Characteristic Declaration, Handles: 0x0001..0x0007
		0210000b000700040008010007000328
			08010007000328
			Bluetooth Attribute Protocol
				Opcode: Read By Type Request (0x08)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..00 1000 = Method: Read By Type Request (0x08)
				Starting Handle: 0x0001
				Ending Handle: 0x0007
				UUID: GATT Characteristic Declaration (0x2803)

<- 801	Rcvd Read By Type Response, Attribute List Length: 3, Device Name, Appearance, Peripheral Preferred Connection Parameters
		0210201b001700040009070200020300002a0400020500012a0600020700042a
			09070200020300002a0400020500012a0600020700042a
			Bluetooth Attribute Protocol
				Opcode: Read By Type Response (0x09)
					0... .... = Authentication Signature: False
					.0.. .... = Command: False
					..00 1001 = Method: Read By Type Response (0x09)
				Length: 7
				Attribute Data, Handle: 0x0002, Characteristic Handle: 0x0003, UUID: Device Name
					Handle: 0x0002 (Generic Access Profile: GATT Characteristic Declaration)
						[Service UUID: Generic Access Profile (0x1800)]
						[UUID: GATT Characteristic Declaration (0x2803)]
					Characteristic Properties: 0x02, Read
					Characteristic Value Handle: 0x0003 (Generic Access Profile: Device Name)
						[Service UUID: Generic Access Profile (0x1800)]
						[UUID: Device Name (0x2a00)]
					UUID: Device Name (0x2a00)
				Attribute Data, Handle: 0x0004, Characteristic Handle: 0x0005, UUID: Appearance
					Handle: 0x0004 (Generic Access Profile: Device Name: GATT Characteristic Declaration)
						[Service UUID: Generic Access Profile (0x1800)]
						[Characteristic UUID: Device Name (0x2a00)]
						[UUID: GATT Characteristic Declaration (0x2803)]
					Characteristic Properties: 0x02, Read
					Characteristic Value Handle: 0x0005 (Generic Access Profile: Appearance)
						[Service UUID: Generic Access Profile (0x1800)]
						[UUID: Appearance (0x2a01)]
					UUID: Appearance (0x2a01)
				Attribute Data, Handle: 0x0006, Characteristic Handle: 0x0007, UUID: Peripheral Preferred Connection Parameters
					Handle: 0x0006 (Generic Access Profile: Appearance: GATT Characteristic Declaration)
						[Service UUID: Generic Access Profile (0x1800)]
						[Characteristic UUID: Appearance (0x2a01)]
						[UUID: GATT Characteristic Declaration (0x2803)]
					Characteristic Properties: 0x02, Read
					Characteristic Value Handle: 0x0007 (Generic Access Profile: Peripheral Preferred Connection Parameters)
						[Service UUID: Generic Access Profile (0x1800)]
						[UUID: Peripheral Preferred Connection Parameters (0x2a04)]
					UUID: Peripheral Preferred Connection Parameters (0x2a04)
				[UUID: GATT Characteristic Declaration (0x2803)]
				[Request in Frame: 799]


```
