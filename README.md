# Flow Rate Testing
- This Code being edited to test the flow rate of a drain pump
- We are using an exisiting pico on a pcb board for solenoids to create a DAQ setup to get results
- We are able to turn on and off the existing pump using buttons attached the the board previously allowing us to be handsoff
- We are using High and low sensors on the edge of the containers to detect when there is or isnt water inside of the container to get a timestamp to compare results
- We are measuring the setup's flow rate by how much water weight is leaving the system using a SL 7510 Series of Selleton Scale
- We originally tried to detect the 4-20mA output for 0 pounds being 4mA and 10,0000 pounds being 20mA from a 150 ohm resistor divider
- The board was not able to detect the small ammount of changed in current to accurately detect weight
- However the derrivative of the line does not change thus the Gallons per minute wont change so the data is useful
- We started to send the data via serial form the db9 port to usb for our laptop but improved the old system first

# Future additions
- Create a more stationary testing station so that the water doesnt have to be in pvc pipes
- Dupont connectors instead of open wires with electrical tape

# Results!
- Worked properly and Mike Fallon recieved the proper data to bring to GE
