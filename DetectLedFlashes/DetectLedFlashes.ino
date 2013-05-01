/* DetectLedFlashes.ino

Read a LDR (Light Dependent Resistor) to detect led flashing on my electricity meter.
Report information back over the usb port.

Schematics: 
Connect one end of the photocell to 5V, the other end to Analog 0.
Then connect one end of a 10K resistor from Analog 0 to ground 
*/
 
const int LDR_PIN = 0;       // the cell and 10K pulldown are connected to a0
const int THRESHOLD = 50;    // Or calibrate in setup

void setup(void) {
	Serial.begin(115200);	// We'll send debugging information via the Serial monitor

        /*
	int photocellReading = analogRead(LDR_PIN);
	int intensity_threshold = photocellReading * 2 + 10;	//Calibrate
        Serial.print("Insensity threshold ");
        Serial.println(intensity_threshold);
        */
}
 
void loop(void) {
	int photocellReading;

	do {
		photocellReading = analogRead(LDR_PIN); 
		delay(1);	//minimal delay
	} while (photocellReading < THRESHOLD);
  
	Serial.print("Led intensity ");
	Serial.println(photocellReading);     // the raw analog reading

	//debounce...
	delay(250); 
	do {
		photocellReading = analogRead(LDR_PIN); 
		delay(1);	//minimal delay
	} while (photocellReading >= THRESHOLD);
}
